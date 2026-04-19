# -*- coding: utf-8 -*-
"""
Tests for CR-8: Workspace, RoleInWorkspace, access helpers, and
WorkspaceSwitchView.

RoleOnObject (object-level grants) is deferred to CR-10 and is not tested here.

All tests use @pytest.mark.django_db and the shared ``admin_user`` fixture
from the root conftest.
"""

import pytest
from django.contrib.auth.models import Group, User

from koalixcrm.core.models.workspace import Workspace
from koalixcrm.core.models.access import Role, RoleInWorkspace
from koalixcrm.core.models.workspace_switch_event import WorkspaceSwitchEvent
from koalixcrm.core.access import effective_roles, permissions_for_role, user_workspaces


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def workspace(db):
    return Workspace.objects.create(name='Test Workspace', color='#ff0000')


@pytest.fixture
def second_workspace(db):
    return Workspace.objects.create(name='Second Workspace', color='#00ff00')


@pytest.fixture
def plain_user(db):
    return User.objects.create_user(username='plain_user', password='pass')


@pytest.fixture
def test_group(db):
    return Group.objects.create(name='test_group')


@pytest.fixture
def second_group(db):
    return Group.objects.create(name='second_group')


# ---------------------------------------------------------------------------
# 1. Workspace creation, __str__, and new fields
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestWorkspace:
    def test_create_and_str(self, workspace):
        assert str(workspace) == 'Test Workspace'

    def test_name_unique(self, workspace):
        with pytest.raises(Exception):
            Workspace.objects.create(name='Test Workspace')

    def test_color_blank_allowed(self, db):
        ws = Workspace.objects.create(name='Colorless Workspace')
        assert ws.color == ''

    def test_organization_optional(self, workspace):
        assert workspace.organization is None

    def test_ordering_by_name(self, db):
        Workspace.objects.create(name='Alpha')
        Workspace.objects.create(name='Zulu')
        names = list(Workspace.objects.values_list('name', flat=True))
        assert names == sorted(names)

    def test_description_default_empty(self, workspace):
        assert workspace.description == ''

    def test_description_can_be_set(self, db):
        ws = Workspace.objects.create(name='Described WS', description='A description')
        assert ws.description == 'A description'

    def test_external_workspace_reference_default_empty(self, workspace):
        assert workspace.external_workspace_reference == ''

    def test_external_workspace_reference_can_be_set(self, db):
        ws = Workspace.objects.create(name='RefWS', external_workspace_reference='REP')
        assert ws.external_workspace_reference == 'REP'

    def test_is_active_default_true(self, workspace):
        assert workspace.is_active is True

    def test_is_active_can_be_set_false(self, db):
        ws = Workspace.objects.create(name='Inactive WS', is_active=False)
        assert ws.is_active is False


# ---------------------------------------------------------------------------
# 2. Role enum
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestRoleEnum:
    def test_seven_values_present(self):
        values = set(Role.values)
        assert values == {
            'admin', 'editor', 'viewer', 'commenter',
            'employee', 'line_manager', 'project_manager',
        }

    def test_db_codes_are_lowercase_snake_case(self):
        # Each Role value (the DB-stored code) must be lowercase snake_case.
        for code in Role.values:
            assert code == code.lower(), f"Role code {code!r} is not lowercase"
            assert ' ' not in code, f"Role code {code!r} contains spaces"


# ---------------------------------------------------------------------------
# 3. RoleInWorkspace unique_together
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestRoleInWorkspace:
    def test_create(self, test_group, workspace):
        riw = RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.ADMIN
        )
        assert str(riw)  # smoke test for __str__

    def test_str_format(self, test_group, workspace):
        riw = RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.ADMIN
        )
        assert 'test_group' in str(riw)
        assert 'Test Workspace' in str(riw)

    def test_unique_together_rejects_duplicate(self, test_group, workspace):
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.VIEWER
        )
        with pytest.raises(Exception):
            RoleInWorkspace.objects.create(
                group=test_group, workspace=workspace, role=Role.VIEWER
            )

    def test_same_group_different_roles_allowed(self, test_group, workspace):
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.VIEWER
        )
        # Adding a different role on the same workspace is allowed.
        riw2 = RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.EDITOR
        )
        assert riw2.pk is not None

    def test_unique_together_is_group_workspace_role(self, test_group, second_group, workspace):
        """Two different groups can both hold the same role in the same workspace."""
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.VIEWER
        )
        riw2 = RoleInWorkspace.objects.create(
            group=second_group, workspace=workspace, role=Role.VIEWER
        )
        assert riw2.pk is not None


# ---------------------------------------------------------------------------
# 4. effective_roles() — workspace-level roles only
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestEffectiveRoles:
    """Test effective_roles() with workspace-level grants only."""

    def test_returns_workspace_level_roles(self, admin_user, test_group, workspace):
        admin_user.groups.add(test_group)
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.EDITOR
        )
        from types import SimpleNamespace
        obj = SimpleNamespace(workspace=workspace)

        roles = effective_roles(admin_user, obj)
        assert Role.EDITOR in roles

    def test_no_workspace_attr_returns_empty_set(self, plain_user):
        """Objects without .workspace gracefully return an empty set."""
        from types import SimpleNamespace
        obj = SimpleNamespace()  # no .workspace attribute

        roles = effective_roles(plain_user, obj)
        assert roles == set()

    def test_user_with_no_group_returns_empty_set(self, plain_user, workspace):
        """User with no group memberships gets an empty set."""
        from types import SimpleNamespace
        obj = SimpleNamespace(workspace=workspace)

        roles = effective_roles(plain_user, obj)
        assert roles == set()

    def test_user_with_group_but_no_grant_returns_empty_set(self, plain_user, test_group, workspace):
        """User in a group that holds no RoleInWorkspace row gets an empty set."""
        plain_user.groups.add(test_group)
        from types import SimpleNamespace
        obj = SimpleNamespace(workspace=workspace)

        roles = effective_roles(plain_user, obj)
        assert roles == set()

    def test_multiple_groups_roles_unioned(self, plain_user, test_group, second_group, workspace):
        """User in two groups with different roles gets the union of both."""
        plain_user.groups.add(test_group, second_group)
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.ADMIN
        )
        RoleInWorkspace.objects.create(
            group=second_group, workspace=workspace, role=Role.VIEWER
        )
        from types import SimpleNamespace
        obj = SimpleNamespace(workspace=workspace)

        roles = effective_roles(plain_user, obj)
        assert Role.ADMIN in roles
        assert Role.VIEWER in roles

    def test_superuser_returns_all_roles(self, admin_user, workspace):
        """Superuser always gets all Role values."""
        admin_user.is_superuser = True
        admin_user.save()
        from types import SimpleNamespace
        obj = SimpleNamespace(workspace=workspace)

        roles = effective_roles(admin_user, obj)
        assert roles == set(Role.values)

    def test_unauthenticated_user_returns_empty(self, workspace):
        """None / unauthenticated user always gets empty set."""
        from types import SimpleNamespace
        obj = SimpleNamespace(workspace=workspace)

        roles = effective_roles(None, obj)
        assert roles == set()

    def test_workspace_none_returns_empty(self, plain_user):
        """Object whose .workspace is None returns empty set."""
        from types import SimpleNamespace
        obj = SimpleNamespace(workspace=None)

        roles = effective_roles(plain_user, obj)
        assert roles == set()


# ---------------------------------------------------------------------------
# 5. user_workspaces()
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestUserWorkspaces:
    def test_returns_workspaces_via_group(self, plain_user, test_group, workspace):
        plain_user.groups.add(test_group)
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.VIEWER
        )
        qs = user_workspaces(plain_user)
        assert workspace in qs

    def test_excludes_inactive_workspaces(self, plain_user, test_group, db):
        inactive_ws = Workspace.objects.create(
            name='Inactive', color='', is_active=False
        )
        plain_user.groups.add(test_group)
        RoleInWorkspace.objects.create(
            group=test_group, workspace=inactive_ws, role=Role.VIEWER
        )
        qs = user_workspaces(plain_user)
        assert inactive_ws not in qs

    def test_superuser_sees_all_active_workspaces(self, admin_user, workspace, second_workspace, db):
        admin_user.is_superuser = True
        admin_user.save()
        inactive_ws = Workspace.objects.create(name='Inactive2', is_active=False)
        qs = user_workspaces(admin_user)
        assert workspace in qs
        assert second_workspace in qs
        assert inactive_ws not in qs

    def test_unauthenticated_returns_none_qs(self, db):
        qs = user_workspaces(None)
        assert qs.count() == 0

    def test_no_duplicates_with_multiple_group_roles(self, plain_user, test_group, second_group, workspace):
        """User in two groups both having roles on the same workspace sees it once."""
        plain_user.groups.add(test_group, second_group)
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.VIEWER
        )
        RoleInWorkspace.objects.create(
            group=second_group, workspace=workspace, role=Role.EDITOR
        )
        qs = user_workspaces(plain_user)
        assert qs.filter(pk=workspace.pk).count() == 1


# ---------------------------------------------------------------------------
# 6. permissions_for_role()
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestPermissionsForRole:
    def test_admin_has_all_perms(self):
        perms = permissions_for_role(Role.ADMIN)
        assert perms == {'add', 'change', 'delete', 'view'}

    def test_editor_perms(self):
        perms = permissions_for_role(Role.EDITOR)
        assert perms == {'add', 'change', 'view'}

    def test_viewer_perms(self):
        perms = permissions_for_role(Role.VIEWER)
        assert perms == {'view'}

    def test_commenter_perms(self):
        perms = permissions_for_role(Role.COMMENTER)
        assert perms == {'view'}

    def test_employee_perms(self):
        perms = permissions_for_role(Role.EMPLOYEE)
        assert perms == {'view'}

    def test_line_manager_perms(self):
        perms = permissions_for_role(Role.LINE_MANAGER)
        assert perms == {'add', 'change', 'view'}

    def test_project_manager_perms(self):
        perms = permissions_for_role(Role.PROJECT_MANAGER)
        assert perms == {'add', 'change', 'view'}

    def test_unknown_role_returns_empty(self):
        perms = permissions_for_role('nonexistent')
        assert perms == set()


# ---------------------------------------------------------------------------
# 7. WorkspaceSwitchView — happy path (group-based)
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestWorkspaceSwitchViewHappyPath:
    def test_switch_sets_session_and_redirects(self, admin_user, test_group, workspace, client):
        admin_user.groups.add(test_group)
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.ADMIN
        )
        client.force_login(admin_user)
        response = client.post(
            '/admin/core/workspace/switch/',
            {'workspace_id': workspace.pk},
        )
        # Should redirect to admin index.
        assert response.status_code == 302
        assert response['Location'].endswith('/admin/')

    def test_switch_writes_session_value(self, admin_user, test_group, workspace, client):
        admin_user.groups.add(test_group)
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.ADMIN
        )
        client.force_login(admin_user)
        client.post(
            '/admin/core/workspace/switch/',
            {'workspace_id': workspace.pk},
        )
        session = client.session
        assert session.get('active_workspace_id') == workspace.pk

    def test_switch_writes_audit_row(self, admin_user, test_group, workspace, second_workspace, client):
        admin_user.groups.add(test_group)
        RoleInWorkspace.objects.create(
            group=test_group, workspace=workspace, role=Role.ADMIN
        )
        RoleInWorkspace.objects.create(
            group=test_group, workspace=second_workspace, role=Role.VIEWER
        )
        client.force_login(admin_user)
        # First switch: workspace
        client.post('/admin/core/workspace/switch/', {'workspace_id': workspace.pk})
        # Second switch: second_workspace (so from_workspace is set)
        client.post('/admin/core/workspace/switch/', {'workspace_id': second_workspace.pk})

        events = WorkspaceSwitchEvent.objects.filter(user=admin_user).order_by('timestamp')
        assert events.count() == 2

        last = events.last()
        assert last.from_workspace_id == workspace.pk
        assert last.to_workspace_id == second_workspace.pk


# ---------------------------------------------------------------------------
# 8. WorkspaceSwitchView — rejects workspace where user has no role
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestWorkspaceSwitchViewUnauthorised:
    def test_switch_to_inaccessible_workspace_returns_403(
        self, workspace, client, db
    ):
        # Use a non-superuser staff member who has no group assignment.
        staff_user = User.objects.create_user(
            username='limited_staff', password='pass', is_staff=True
        )
        client.force_login(staff_user)
        # No group / RoleInWorkspace row — user has no access.
        response = client.post(
            '/admin/core/workspace/switch/',
            {'workspace_id': workspace.pk},
        )
        assert response.status_code == 403

    def test_unauthenticated_request_redirects(self, workspace, client):
        response = client.post(
            '/admin/core/workspace/switch/',
            {'workspace_id': workspace.pk},
        )
        # staff_member_required redirects to login.
        assert response.status_code in (302, 403)
