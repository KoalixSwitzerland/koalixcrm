# -*- coding: utf-8 -*-
from __future__ import annotations

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'koalixcrm.core'
    label = 'core'
    default_auto_field = 'django.db.models.BigAutoField'
    required_peers: tuple[str, ...] = ()
    optional_peers: tuple[str, ...] = ('koalixcrm.accounting',)

    def ready(self) -> None:
        import koalixcrm.core.signals.pdf_export_signals  # noqa: F401
        from koalixcrm.core.app_checks import register_peer_check
        register_peer_check(self)

        _enforce_workspace_authorization()


_workspace_permission_patched = False


def _enforce_workspace_authorization() -> None:
    """Make every DRF view authorize the ``workspace_id`` segment of its URL.

    Org ADR-0008 line 3 / org ADR-0013 layer 0; specified by REQ-0028.

    Every REST app is mounted under ``/<service>/api/v1/<workspace_id>/``, the
    segment is caller-controlled, and the scoping so far came from the session
    alone. The declared permission classes are organisation-wide Django model
    rights, which structurally cannot express a tenant. So the check is
    installed centrally rather than added to each viewset's
    ``permission_classes``: REQ-0028 AC-5 requires that a view added later,
    which knows nothing about this requirement, is covered the moment it is
    mounted under the prefix. An explicit per-view list drifts, and a drifted
    entry serves another tenant silently.

    ``check_permissions`` rather than ``get_permissions``: viewsets that
    override the latter return a fresh list and would drop an appended entry
    on the floor. Nothing overrides ``check_permissions``, and DRF calls it on
    every request.

    Four conditions, all of them because this package ships open-source on
    PyPI and is embedded in projects we do not control:

    (a) patched only from ``CoreConfig.ready()`` — an embedder who does not
        install ``koalixcrm.core`` gets an unmodified DRF;
    (b) idempotent via the module-level flag, so a second ``ready()`` (test
        runners re-populating the app registry) does not stack the wrapper;
    (c) it *chains* the implementation it found instead of replacing it, so it
        coexists with another patch on the same method;
    (d) the guard runs *before* the chained implementation, so a caller with
        neither a role in the workspace nor the model permission is told about
        the workspace rather than about the model (AC-7). Unauthenticated
        callers are unaffected by the ordering: ``permission_denied()`` raises
        ``NotAuthenticated`` whenever authenticators are configured and none
        succeeded, so they still get 401 rather than 403.
    """
    global _workspace_permission_patched
    if _workspace_permission_patched:
        return
    _workspace_permission_patched = True

    from rest_framework.views import APIView

    from koalixcrm.shared.permissions import WorkspaceMembershipPermission

    previous_check_permissions = APIView.check_permissions

    def check_permissions(self, request) -> None:
        guard = WorkspaceMembershipPermission()
        if not guard.has_permission(request, self):
            self.permission_denied(
                request,
                message=getattr(guard, 'message', None),
                code=getattr(guard, 'code', None),
            )
        previous_check_permissions(self, request)

    APIView.check_permissions = check_permissions
