# -*- coding: utf-8 -*-
"""
WorkspaceContextMiddleware — activates the session-stored workspace for the
duration of each request.

CR-9 §9.3.
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
            request.active_workspace = None
            return self.get_response(request)

        workspace = self._resolve_workspace(request)
        request.active_workspace = workspace

        if workspace is not None:
            activate_workspace(workspace)
        try:
            response = self.get_response(request)
        finally:
            if workspace is not None:
                deactivate_workspace()

        return response

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
