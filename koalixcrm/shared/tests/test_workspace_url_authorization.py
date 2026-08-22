# -*- coding: utf-8 -*-
"""Unit tests for the `<workspace_id>` URL authorization layer (REQ-0028).

Org ADR-0008 line 3 / org ADR-0013 layer 0, koalixcrm#428.

The route used throughout is the contracts list, because `Contract` is an
ordinary `WorkspaceScopedModel` with a factory. Nothing here is specific to
contracts: the guard is injected into `APIView.check_permissions` from
`CoreConfig.ready()` and keys on the URL kwarg alone.
"""
from __future__ import annotations

import pytest
from django.contrib.auth.models import Group, Permission, User
from rest_framework.test import APIClient

from koalixcrm.contracts.models.contract import Contract
from koalixcrm.contracts.tests.factories.contract_factory import StandardContractFactory
from koalixcrm.core.models.access import Role, RoleInWorkspace
from koalixcrm.core.models.workspace import Workspace

CONTRACTS_URL = '/koalixcrm_contracts/api/v1/{workspace_id}/contracts/'


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def workspace_a(db) -> Workspace:
    return Workspace.objects.create(name='Workspace A', is_active=True)


@pytest.fixture
def workspace_b(db) -> Workspace:
    return Workspace.objects.create(name='Workspace B', is_active=True)


def _grant_all_contract_model_permissions(group: Group) -> None:
    """Give the group every org-wide `contracts.*_contract` right.

    The point of the negative tests is that org-wide model rights are *not*
    enough: the caller below is fully entitled to touch contracts and is still
    refused workspace B.
    """
    permissions = Permission.objects.filter(
        content_type__app_label=Contract._meta.app_label,
        codename__in=(
            'view_contract', 'add_contract',
            'change_contract', 'delete_contract',
        ),
    )
    assert permissions.count() == 4, 'contract model permissions missing from the test DB'
    group.permissions.add(*permissions)


@pytest.fixture
def member_of_a(db, workspace_a) -> User:
    user = User.objects.create_user(username='member_a', password='pw')
    group = Group.objects.create(name='grp_a')
    _grant_all_contract_model_permissions(group)
    user.groups.add(group)
    RoleInWorkspace.objects.create(group=group, workspace=workspace_a, role=Role.ADMIN)
    return user


@pytest.fixture
def member_of_a_and_b(db, workspace_a, workspace_b) -> User:
    user = User.objects.create_user(username='member_ab', password='pw')
    group = Group.objects.create(name='grp_ab')
    _grant_all_contract_model_permissions(group)
    user.groups.add(group)
    RoleInWorkspace.objects.create(group=group, workspace=workspace_a, role=Role.ADMIN)
    RoleInWorkspace.objects.create(group=group, workspace=workspace_b, role=Role.ADMIN)
    return user


@pytest.fixture
def service_account(db, settings) -> User:
    """The non-interactive M2M account: group membership only, no role rows."""
    settings.M2M_MICROSERVICE_GROUP_NAME = 'koalixcrm-microservices'
    user = User.objects.create_user(username='svc-worker', password='pw')
    assert user.is_superuser is False
    group = Group.objects.create(name='koalixcrm-microservices')
    _grant_all_contract_model_permissions(group)
    user.groups.add(group)
    return user


def _client(user: User | None = None) -> APIClient:
    client = APIClient()
    if user is not None:
        client.force_authenticate(user=user)
    return client


# ---------------------------------------------------------------------------
# roles_in_workspace() — the canonical resolution point
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestRolesInWorkspace:
    def test_role_holder_gets_their_roles(self, member_of_a, workspace_a):
        from koalixcrm.core.access import roles_in_workspace
        assert roles_in_workspace(member_of_a, workspace_a.pk) == {Role.ADMIN}

    def test_foreign_workspace_is_empty(self, member_of_a, workspace_b):
        from koalixcrm.core.access import roles_in_workspace
        assert roles_in_workspace(member_of_a, workspace_b.pk) == set()

    def test_inactive_workspace_is_empty_for_role_holder(self, member_of_a, workspace_a):
        from koalixcrm.core.access import roles_in_workspace
        workspace_a.is_active = False
        workspace_a.save()
        assert roles_in_workspace(member_of_a, workspace_a.pk) == set()

    def test_superuser_gets_all_roles_in_an_active_workspace(self, admin_user, workspace_a):
        from koalixcrm.core.access import roles_in_workspace
        assert roles_in_workspace(admin_user, workspace_a.pk) == set(Role.values)

    def test_superuser_gets_nothing_for_inactive_workspace(self, admin_user, workspace_a):
        """AC-2/AC-7: the exemption is from the role check, not from the tenant."""
        from koalixcrm.core.access import roles_in_workspace
        workspace_a.is_active = False
        workspace_a.save()
        assert roles_in_workspace(admin_user, workspace_a.pk) == set()

    def test_superuser_gets_nothing_for_missing_workspace(self, admin_user, workspace_a):
        from koalixcrm.core.access import roles_in_workspace
        assert roles_in_workspace(admin_user, workspace_a.pk + 9999) == set()

    def test_service_account_reaches_workspace_without_a_role_row(
        self, service_account, workspace_a
    ):
        """AC-8: recognised by group membership, holds no RoleInWorkspace row."""
        from koalixcrm.core.access import roles_in_workspace
        assert not RoleInWorkspace.objects.filter(
            group__in=service_account.groups.all()
        ).exists()
        assert roles_in_workspace(service_account, workspace_a.pk) == set(Role.values)

    def test_unset_setting_confers_nothing(self, service_account, workspace_a, settings):
        """AC-8: unset key → nobody is an unrestricted actor through that branch."""
        from koalixcrm.core.access import is_unrestricted_actor, roles_in_workspace
        settings.M2M_MICROSERVICE_GROUP_NAME = ''
        assert is_unrestricted_actor(service_account) is False
        assert roles_in_workspace(service_account, workspace_a.pk) == set()

    def test_nonexistent_group_name_does_not_raise(self, workspace_a, settings, member_of_a):
        """AC-8: a settings key naming no existing group is inert, not fatal."""
        from koalixcrm.core.access import is_unrestricted_actor
        settings.M2M_MICROSERVICE_GROUP_NAME = 'no-such-group-anywhere'
        assert is_unrestricted_actor(member_of_a) is False

    def test_non_member_gains_nothing_from_the_branch(self, member_of_a, workspace_b, settings):
        """AC-8: a user outside the group is still refused workspace B."""
        from koalixcrm.core.access import roles_in_workspace
        settings.M2M_MICROSERVICE_GROUP_NAME = 'koalixcrm-microservices'
        Group.objects.create(name='koalixcrm-microservices')
        assert roles_in_workspace(member_of_a, workspace_b.pk) == set()

    def test_effective_roles_delegates(self, member_of_a, workspace_a):
        """AC-5: one query site. effective_roles must go through roles_in_workspace."""
        from types import SimpleNamespace
        from unittest import mock

        import koalixcrm.core.access as access

        obj = SimpleNamespace(workspace=workspace_a)
        with mock.patch.object(
            access, 'roles_in_workspace', return_value={'sentinel'}
        ) as delegate:
            assert access.effective_roles(member_of_a, obj) == {'sentinel'}
        delegate.assert_called_once_with(member_of_a, workspace_a.pk)


# ---------------------------------------------------------------------------
# the injection itself
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestGuardIsInForce:
    def test_check_permissions_is_patched(self):
        """AC-5: the guard is installed centrally, not declared per view."""
        import koalixcrm.core.apps as core_apps
        from rest_framework.views import APIView

        assert core_apps._workspace_permission_patched is True
        assert APIView.check_permissions.__module__ == core_apps.__name__

    def test_patch_is_idempotent(self):
        from rest_framework.views import APIView

        from koalixcrm.core.apps import _enforce_workspace_authorization

        before = APIView.check_permissions
        _enforce_workspace_authorization()
        assert APIView.check_permissions is before

    def test_undeclared_viewset_is_still_guarded(self, member_of_a, workspace_b):
        """AC-5: ContractViewSet never names WorkspaceMembershipPermission."""
        from koalixcrm.contracts.views.contract_view_set import ContractViewSet
        from koalixcrm.shared.permissions import WorkspaceMembershipPermission

        assert WorkspaceMembershipPermission not in ContractViewSet.permission_classes

        response = _client(member_of_a).get(CONTRACTS_URL.format(workspace_id=workspace_b.pk))
        assert response.status_code == 403

    def test_route_without_workspace_kwarg_is_untouched(self, member_of_a):
        """AC-4: no `workspace_id` kwarg → the layer is inert."""
        from koalixcrm.shared.permissions import WorkspaceMembershipPermission

        class _View:
            kwargs: dict = {}

        assert WorkspaceMembershipPermission().has_permission(None, _View()) is True


# ---------------------------------------------------------------------------
# end-to-end through the URL conf
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestCrossWorkspaceRejection:
    def test_own_workspace_is_admitted(self, member_of_a, workspace_a):
        StandardContractFactory(workspace=workspace_a)
        response = _client(member_of_a).get(CONTRACTS_URL.format(workspace_id=workspace_a.pk))
        assert response.status_code < 400

    @pytest.mark.parametrize('method', ['get', 'post', 'put', 'patch', 'delete'])
    def test_foreign_workspace_is_refused_for_every_method(
        self, member_of_a, workspace_b, method
    ):
        """AC-2. The caller holds every org-wide contract permission."""
        contract = StandardContractFactory(workspace=workspace_b)
        url = CONTRACTS_URL.format(workspace_id=workspace_b.pk)
        if method in ('put', 'patch', 'delete'):
            url = f'{url}{contract.pk}/'

        before = list(Contract.objects.values_list('pk', 'workspace_id'))
        response = getattr(_client(member_of_a), method)(url, {}, format='json')

        assert response.status_code == 403
        # AC-2: a refused write leaves the data untouched.
        assert list(Contract.objects.values_list('pk', 'workspace_id')) == before

    def test_nonexistent_workspace_is_403_not_404(self, member_of_a, workspace_a):
        response = _client(member_of_a).get(
            CONTRACTS_URL.format(workspace_id=workspace_a.pk + 9999)
        )
        assert response.status_code == 403

    def test_inactive_workspace_is_403(self, member_of_a, workspace_a):
        workspace_a.is_active = False
        workspace_a.save()
        response = _client(member_of_a).get(CONTRACTS_URL.format(workspace_id=workspace_a.pk))
        assert response.status_code == 403

    def test_superuser_is_refused_an_inactive_workspace(self, admin_user, workspace_a):
        """AC-2/AC-7: the exemption does not widen the reachable set."""
        workspace_a.is_active = False
        workspace_a.save()
        response = _client(admin_user).get(CONTRACTS_URL.format(workspace_id=workspace_a.pk))
        assert response.status_code == 403

    def test_refusal_leaks_no_rows_from_the_other_workspace(
        self, member_of_a, workspace_a, workspace_b
    ):
        """AC-3: a refused /<B>/ request returns nothing from A."""
        contract_a = StandardContractFactory(workspace=workspace_a)
        response = _client(member_of_a).get(CONTRACTS_URL.format(workspace_id=workspace_b.pk))
        assert response.status_code == 403
        assert str(contract_a.pk) not in response.content.decode()

    def test_read_does_not_create_a_workspace(self, member_of_a, workspace_a):
        """AC-10: a GET must never mint a tenant row."""
        before = set(Workspace.objects.values_list('pk', flat=True))
        _client(member_of_a).get(CONTRACTS_URL.format(workspace_id=workspace_a.pk))
        assert set(Workspace.objects.values_list('pk', flat=True)) == before

    def test_superuser_read_does_not_create_default_workspace(self, admin_user, workspace_a):
        """AC-10: this is the path that used to call get_or_create()."""
        # A 'Default Workspace' row already exists — contacts migration 0011
        # stamps pre-workspace rows with it — so the assertion is on the *set*
        # of workspaces, not on the absence of that name.
        before = set(Workspace.objects.values_list('pk', flat=True))
        response = _client(admin_user).get(CONTRACTS_URL.format(workspace_id=workspace_a.pk))
        assert response.status_code < 400
        assert set(Workspace.objects.values_list('pk', flat=True)) == before


@pytest.mark.django_db
class TestUrlWorkspaceBeatsSession:
    def test_session_a_url_b_returns_bs_rows(
        self, member_of_a_and_b, workspace_a, workspace_b
    ):
        """AC-3, the core of the middleware correction.

        Without the URL taking precedence over the session ContextVar, the
        mixin's `.filter(workspace=B)` intersects with an activated A and the
        answer is 200 with zero rows — right status, wrong data.
        """
        StandardContractFactory(workspace=workspace_a)
        contract_b = StandardContractFactory(workspace=workspace_b)

        client = APIClient()
        assert client.login(username='member_ab', password='pw')
        session = client.session
        session['active_workspace_id'] = workspace_a.pk
        session.save()

        response = client.get(CONTRACTS_URL.format(workspace_id=workspace_b.pk))

        assert response.status_code == 200
        results = response.json()['results']
        assert results, 'URL workspace B has rows; an empty 200 is the silent-wrong-answer bug'
        assert {row['id'] for row in results} == {contract_b.pk}

        # AC-3: addressing B by URL does not repoint the session.
        assert client.session.get('active_workspace_id') == workspace_a.pk


@pytest.mark.django_db
class TestUnrestrictedActorsAreStillFiltered:
    def test_superuser_list_is_confined_to_the_url_workspace(
        self, admin_user, workspace_a, workspace_b
    ):
        """AC-9: passing the gate does not widen the data space."""
        contract_a = StandardContractFactory(workspace=workspace_a)
        StandardContractFactory(workspace=workspace_b)

        response = _client(admin_user).get(CONTRACTS_URL.format(workspace_id=workspace_a.pk))

        assert response.status_code == 200
        assert {row['id'] for row in response.json()['results']} == {contract_a.pk}

    def test_service_account_list_is_confined_to_the_url_workspace(
        self, service_account, workspace_a, workspace_b
    ):
        contract_a = StandardContractFactory(workspace=workspace_a)
        StandardContractFactory(workspace=workspace_b)

        response = _client(service_account).get(
            CONTRACTS_URL.format(workspace_id=workspace_a.pk)
        )

        assert response.status_code == 200
        assert {row['id'] for row in response.json()['results']} == {contract_a.pk}


@pytest.mark.django_db
class TestStockViewsDeclareModelPermissions:
    """AC-6: no view under a `<workspace_id>` prefix declares IsAuthenticated alone."""

    def test_three_stock_views_carry_a_model_permission_class(self):
        from rest_framework.permissions import IsAuthenticated

        from koalixcrm.stock.views.bill_of_materials_explosion_view_set import (
            BillOfMaterialsExplosionViewSet,
        )
        from koalixcrm.stock.views.scan_resolve_view import ScanResolveView
        from koalixcrm.stock.views.serial_unit_availability_view import (
            SerialUnitAvailabilityView,
        )

        for view in (
            BillOfMaterialsExplosionViewSet,
            SerialUnitAvailabilityView,
            ScanResolveView,
        ):
            assert view.permission_classes != [IsAuthenticated], view.__name__
            assert len(view.permission_classes) > 1, view.__name__


@pytest.mark.django_db
class TestOrderingAndUnauthenticated:
    def test_unauthenticated_gets_401_not_403(self, workspace_a):
        """AC-7. `permission_denied()` raises NotAuthenticated when
        authenticators are configured and none succeeded — but DRF downgrades
        that to 403 unless the first authenticator advertises a scheme, which
        is why `CeleryWorkerM2MAuthentication` now defines
        `authenticate_header()`.
        """
        response = APIClient().get(CONTRACTS_URL.format(workspace_id=workspace_a.pk))
        assert response.status_code == 401

    def test_workspace_is_named_before_the_model_permission(self, db, workspace_a, workspace_b):
        """AC-7: a caller with neither the role nor the model right is told
        about the workspace, not about the model."""
        from koalixcrm.shared.permissions import WorkspaceMembershipPermission

        user = User.objects.create_user(username='no_rights', password='pw')
        group = Group.objects.create(name='grp_no_rights')
        user.groups.add(group)
        RoleInWorkspace.objects.create(group=group, workspace=workspace_a, role=Role.VIEWER)
        assert not user.has_perm(f'{Contract._meta.app_label}.view_contract')

        response = _client(user).get(CONTRACTS_URL.format(workspace_id=workspace_b.pk))

        assert response.status_code == 403
        assert response.data['detail'] == WorkspaceMembershipPermission.message
