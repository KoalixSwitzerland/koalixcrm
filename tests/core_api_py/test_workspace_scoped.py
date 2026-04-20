# -*- coding: utf-8 -*-
"""
Tests for CR-9: WorkspaceAwareManager, workspace_context, WorkspaceContextMiddleware,
WorkspaceScopedModelAdmin.save_model, and PDFExportProcess workspace scoping.
"""

import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory

from koalixcrm.core.managers.workspace_aware import (
    WorkspaceContextMissing,
    activate_workspace,
    deactivate_workspace,
    get_active_workspace,
    workspace_context,
    WorkspaceAwareManager,
)
from koalixcrm.core.models.workspace import Workspace


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def ws_a(db):
    return Workspace.objects.create(name='Workspace A', is_active=True)


@pytest.fixture
def ws_b(db):
    return Workspace.objects.create(name='Workspace B', is_active=True)


@pytest.fixture(autouse=True)
def clean_context():
    """Ensure context variable is cleared between tests."""
    deactivate_workspace()
    yield
    deactivate_workspace()


# ---------------------------------------------------------------------------
# 1. WorkspaceAwareManager.get_queryset — with / without context
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestWorkspaceAwareManagerGetQueryset:

    def test_unscoped_when_no_active_workspace(self, ws_a, ws_b):
        """Without an active workspace, manager returns unfiltered queryset."""
        qs = Workspace.objects.all()
        pks = list(qs.values_list('pk', flat=True))
        assert ws_a.pk in pks
        assert ws_b.pk in pks

    def test_scoped_when_active_workspace_set(self, ws_a, ws_b):
        """
        WorkspaceAwareManager on a workspace-scoped model filters by active workspace.
        We use PDFExportProcess directly for this.
        """
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess

        proc_a = PDFExportProcess.objects.create(
            workspace=ws_a,
            source_model='TestModel',
            source_id=1,
        )
        proc_b = PDFExportProcess.objects.create(
            workspace=ws_b,
            source_model='TestModel',
            source_id=2,
        )

        activate_workspace(ws_a)
        qs = PDFExportProcess.objects.all()
        pks = list(qs.values_list('pk', flat=True))
        assert proc_a.pk in pks
        assert proc_b.pk not in pks


# ---------------------------------------------------------------------------
# 2. raise_on_missing_context=True branch
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestRaiseOnMissingContext:

    def test_raises_when_no_context_and_flag_true(self):
        class StrictManager(WorkspaceAwareManager):
            raise_on_missing_context = True

        # Bind manager to PDFExportProcess temporarily
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        manager = StrictManager()
        manager.model = PDFExportProcess
        manager.auto_created = True
        manager._db = None
        manager._hints = {}

        with pytest.raises(WorkspaceContextMissing):
            manager.get_queryset()

    def test_no_raise_when_context_set(self, ws_a):
        class StrictManager(WorkspaceAwareManager):
            raise_on_missing_context = True

        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        manager = StrictManager()
        manager.model = PDFExportProcess
        manager.auto_created = True
        manager._db = None
        manager._hints = {}

        activate_workspace(ws_a)
        # Should not raise
        qs = manager.get_queryset()
        assert qs is not None


# ---------------------------------------------------------------------------
# 3. workspace_context() context manager
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestWorkspaceContextManager:

    def test_activates_workspace_inside_block(self, ws_a):
        assert get_active_workspace() is None
        with workspace_context(ws_a):
            assert get_active_workspace() == ws_a

    def test_deactivates_workspace_after_block(self, ws_a):
        with workspace_context(ws_a):
            pass
        assert get_active_workspace() is None

    def test_restores_previous_context_after_nested_exit(self, ws_a, ws_b):
        activate_workspace(ws_a)
        with workspace_context(ws_b):
            assert get_active_workspace() == ws_b
        assert get_active_workspace() == ws_a

    def test_deactivates_on_exception(self, ws_a):
        try:
            with workspace_context(ws_a):
                raise ValueError('oops')
        except ValueError:
            pass
        assert get_active_workspace() is None


# ---------------------------------------------------------------------------
# 4. WorkspaceContextMiddleware via RequestFactory
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestWorkspaceContextMiddleware:

    def _make_request(self, user, session_data=None):
        factory = RequestFactory()
        request = factory.get('/')
        request.user = user
        request.session = dict(session_data or {})
        return request

    def _run_middleware(self, request):
        from koalixcrm.core.middleware.workspace_context import WorkspaceContextMiddleware

        responses = []

        def get_response(req):
            # Capture active workspace inside the view.
            from koalixcrm.core.managers.workspace_aware import get_active_workspace
            responses.append(get_active_workspace())
            return object()

        mw = WorkspaceContextMiddleware(get_response)
        mw(request)
        return responses[0] if responses else None

    def test_single_workspace_auto_activates(self, ws_a):
        from django.contrib.auth.models import Group
        from koalixcrm.core.models.access import RoleInWorkspace, Role

        user = User.objects.create_user(username='u_single', password='pass', is_staff=True)
        group = Group.objects.create(name='g_single')
        user.groups.add(group)
        RoleInWorkspace.objects.create(group=group, workspace=ws_a, role=Role.VIEWER)

        request = self._make_request(user)
        active_in_view = self._run_middleware(request)

        assert active_in_view == ws_a
        assert request.active_workspace == ws_a
        assert request.session.get('active_workspace_id') == ws_a.pk

    def test_multiple_workspaces_picks_lowest_pk(self, ws_a, ws_b):
        from django.contrib.auth.models import Group
        from koalixcrm.core.models.access import RoleInWorkspace, Role

        user = User.objects.create_user(username='u_multi', password='pass', is_staff=True)
        group = Group.objects.create(name='g_multi')
        user.groups.add(group)
        RoleInWorkspace.objects.create(group=group, workspace=ws_a, role=Role.VIEWER)
        RoleInWorkspace.objects.create(group=group, workspace=ws_b, role=Role.VIEWER)

        request = self._make_request(user)
        active_in_view = self._run_middleware(request)

        expected = ws_a if ws_a.pk < ws_b.pk else ws_b
        assert active_in_view == expected

    def test_no_workspaces_sets_none(self):
        user = User.objects.create_user(username='u_none', password='pass', is_staff=True)
        request = self._make_request(user)
        active_in_view = self._run_middleware(request)

        assert active_in_view is None
        assert request.active_workspace is None

    def test_session_workspace_id_used_when_valid(self, ws_a, ws_b):
        from django.contrib.auth.models import Group
        from koalixcrm.core.models.access import RoleInWorkspace, Role

        user = User.objects.create_user(username='u_session', password='pass', is_staff=True)
        group = Group.objects.create(name='g_session')
        user.groups.add(group)
        RoleInWorkspace.objects.create(group=group, workspace=ws_a, role=Role.VIEWER)
        RoleInWorkspace.objects.create(group=group, workspace=ws_b, role=Role.VIEWER)

        request = self._make_request(user, {'active_workspace_id': ws_b.pk})
        active_in_view = self._run_middleware(request)

        assert active_in_view == ws_b

    def test_unauthenticated_request_skipped(self):
        from django.contrib.auth.models import AnonymousUser
        from koalixcrm.core.middleware.workspace_context import WorkspaceContextMiddleware

        called_with = []

        def get_response(req):
            called_with.append(getattr(req, 'active_workspace', 'NOT_SET'))
            return object()

        mw = WorkspaceContextMiddleware(get_response)
        factory = RequestFactory()
        request = factory.get('/')
        request.user = AnonymousUser()
        request.session = {}
        mw(request)

        # Middleware sets active_workspace=None on every request (including
        # anonymous) so viewsets can rely on the attribute always existing.
        assert called_with[0] is None


# ---------------------------------------------------------------------------
# 5. WorkspaceScopedModelAdmin.save_model — mismatched workspace raises
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestWorkspaceScopedModelAdminSaveModel:

    def _make_admin(self, model_class):
        from django.contrib.admin import site
        from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
        from django.contrib.admin import ModelAdmin

        class ScopedAdmin(WorkspaceScopedModelAdmin, ModelAdmin):
            pass

        return ScopedAdmin(model_class, site)

    def test_save_assigns_workspace_when_none(self, ws_a):
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess

        admin = self._make_admin(PDFExportProcess)

        user = User.objects.create_user(username='u_save', password='pass', is_staff=True)
        factory = RequestFactory()
        request = factory.get('/')
        request.user = user
        request.active_workspace = ws_a

        obj = PDFExportProcess(source_model='Invoice', source_id=42)
        assert obj.workspace_id is None

        # We override super().save_model to avoid DB write in this unit test.
        from unittest.mock import patch
        with patch.object(type(admin).__mro__[-3], 'save_model', lambda *a, **k: None):
            admin.save_model(request, obj, None, False)

        assert obj.workspace_id == ws_a.id

    def test_save_raises_on_mismatched_workspace(self, ws_a, ws_b):
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        from django.core.exceptions import PermissionDenied

        admin = self._make_admin(PDFExportProcess)

        user = User.objects.create_user(username='u_mismatch', password='pass', is_staff=True)
        factory = RequestFactory()
        request = factory.get('/')
        request.user = user
        request.active_workspace = ws_a  # active = ws_a

        obj = PDFExportProcess(source_model='Invoice', source_id=1)
        obj.workspace_id = ws_b.id  # but obj belongs to ws_b

        with pytest.raises(PermissionDenied):
            admin.save_model(request, obj, None, False)

    def test_superuser_bypasses_workspace_check(self, ws_a, ws_b, admin_user):
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        from unittest.mock import patch

        admin_obj = self._make_admin(PDFExportProcess)

        factory = RequestFactory()
        request = factory.get('/')
        request.user = admin_user  # is_superuser=True
        request.active_workspace = ws_a

        obj = PDFExportProcess(source_model='Invoice', source_id=1)
        obj.workspace_id = ws_b.id  # mismatch, but superuser

        with patch.object(type(admin_obj).__mro__[-3], 'save_model', lambda *a, **k: None):
            # Should not raise
            admin_obj.save_model(request, obj, None, False)


# ---------------------------------------------------------------------------
# 6. PDFExportProcess is workspace-scoped
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestPDFExportProcessWorkspaceScoped:

    def test_create_and_filter(self, ws_a, ws_b):
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess

        proc_a = PDFExportProcess.objects.create(
            workspace=ws_a,
            source_model='Invoice',
            source_id=10,
        )
        PDFExportProcess.objects.create(
            workspace=ws_b,
            source_model='Invoice',
            source_id=20,
        )

        activate_workspace(ws_a)
        qs = PDFExportProcess.objects.all()
        assert proc_a.pk in list(qs.values_list('pk', flat=True))

    def test_workspace_field_exists(self, ws_a):
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess

        proc = PDFExportProcess.objects.create(
            workspace=ws_a,
            source_model='Quotation',
            source_id=5,
        )
        proc.refresh_from_db()
        assert proc.workspace_id == ws_a.pk

    def test_visible_to_returns_correct_rows(self, ws_a, ws_b):
        from koalixcrm.core.models.pdf_export_process import PDFExportProcess
        from django.contrib.auth.models import Group
        from koalixcrm.core.models.access import RoleInWorkspace, Role

        user = User.objects.create_user(username='u_visible', password='pass')
        group = Group.objects.create(name='g_visible')
        user.groups.add(group)
        RoleInWorkspace.objects.create(group=group, workspace=ws_a, role=Role.VIEWER)

        proc_a = PDFExportProcess.objects.create(
            workspace=ws_a, source_model='M', source_id=1
        )
        proc_b = PDFExportProcess.objects.create(
            workspace=ws_b, source_model='M', source_id=2
        )

        visible = PDFExportProcess.objects.visible_to(user)
        pks = list(visible.values_list('pk', flat=True))
        assert proc_a.pk in pks
        assert proc_b.pk not in pks
