# -*- coding: utf-8 -*-
"""
WorkspaceContextMiddleware — activates the workspace in force for the duration
of each request.

Two sources, in this precedence: the ``workspace_id`` kwarg of the resolved
URL, then the session (CR-9 §9.3).

REQ-0028 makes the URL authoritative here rather than in
``WorkspaceScopedViewSetMixin``, for two reasons that a mixin-level fix does
not reach:

  * ``WorkspaceScopedModel.objects`` is a ``WorkspaceAwareManager`` filtering
    on the ContextVar this middleware activates. A mixin-level
    ``.filter(workspace=B)`` therefore *intersects* with an activated session
    workspace A and yields 200 with zero rows — a silent wrong answer rather
    than an error (AC-3 explicitly rules that out).
  * 20 view modules read ``request.active_workspace`` directly instead of
    going through the mixin.

Setting both ``request.active_workspace`` and the ContextVar corrects every
one of those call sites at once.

This middleware decides only *which* workspace is in force, never *whether*
the caller may reach it. ``process_view`` runs before the view while DRF
authenticates inside it, so on token and M2M requests the user here is still
``AnonymousUser``; the membership decision belongs to
``WorkspaceMembershipPermission``, which runs inside DRF's dispatch where the
user is known.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from koalixcrm.core.managers.workspace_aware import (
    activate_workspace,
    deactivate_workspace,
)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    from koalixcrm.core.models.workspace import Workspace


class WorkspaceContextMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not getattr(request, 'user', None) or not request.user.is_authenticated:
            workspace = None
        else:
            workspace = self._resolve_workspace(request)

        request.active_workspace = workspace

        if workspace is not None:
            activate_workspace(workspace)
        try:
            return self.get_response(request)
        finally:
            # Unconditional: ``process_view`` may have activated a workspace
            # (from the URL) that ``__call__`` never saw.
            deactivate_workspace()

    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable[..., HttpResponse],
        view_args: tuple,
        view_kwargs: dict,
    ) -> None:
        """Let the resolved URL's ``workspace_id`` override the session value.

        Runs after URL resolution and before the view, which is the first
        point at which the URL kwargs are known. A ``workspace_id`` that names
        no active workspace is *not* substituted by anything — the request is
        left without a workspace and ``WorkspaceMembershipPermission`` turns
        that into a 403 (REQ-0028 AC-2, AC-10).

        ``session['active_workspace_id']`` is deliberately not written here:
        addressing a workspace by URL must not silently repoint the session
        (AC-3).
        """
        from koalixcrm.core.models.workspace import Workspace

        workspace_id = (view_kwargs or {}).get('workspace_id')
        if workspace_id is None:
            return None

        try:
            workspace = Workspace.objects.filter(pk=workspace_id, is_active=True).first()
        except (TypeError, ValueError):
            workspace = None

        request.active_workspace = workspace
        if workspace is not None:
            activate_workspace(workspace)
        else:
            deactivate_workspace()
        return None

    def _resolve_workspace(self, request: HttpRequest) -> Workspace | None:
        from koalixcrm.core.access import user_workspaces
        from koalixcrm.core.models.workspace import Workspace

        ws_id = request.session.get('active_workspace_id')
        if ws_id is not None:
            try:
                ws = Workspace.objects.get(pk=ws_id, is_active=True)
                return ws
            except Workspace.DoesNotExist:
                pass

        # No valid session value — pick a default from accessible workspaces.
        accessible = list(user_workspaces(request.user).order_by('pk')[:2])
        if not accessible:
            return None

        ws = accessible[0]  # min(pk) first due to order_by('pk')
        request.session['active_workspace_id'] = ws.pk
        return ws
