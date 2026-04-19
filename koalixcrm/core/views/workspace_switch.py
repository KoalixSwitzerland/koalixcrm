# -*- coding: utf-8 -*-
"""
WorkspaceSwitchView — POST endpoint that sets the active workspace in the
session, writes an audit row, and redirects to the admin index.

CR-8 §8.6.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(staff_member_required, name='dispatch')
class WorkspaceSwitchView(View):
    """POST-only view.

    POST parameters:
        workspace_id (int) — the pk of the Workspace to switch to.

    On success: sets session['active_workspace_id'], writes WorkspaceSwitchEvent,
    redirects to admin:index.
    On failure: raises PermissionDenied (403) if the user holds no
    RoleInWorkspace for the requested workspace.
    """

    http_method_names = ['post']

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            raise PermissionDenied

        workspace_id_raw = request.POST.get('workspace_id')
        if not workspace_id_raw:
            raise PermissionDenied('workspace_id is required')

        try:
            workspace_id = int(workspace_id_raw)
        except (ValueError, TypeError):
            raise PermissionDenied('workspace_id must be an integer')

        from koalixcrm.core.access import user_workspaces
        from koalixcrm.core.models.workspace_switch_event import WorkspaceSwitchEvent

        # Authorisation: the user must have access to the requested workspace
        # (via group membership or superuser status).
        has_access = user_workspaces(request.user).filter(pk=workspace_id).exists()

        if not has_access:
            raise PermissionDenied(
                'You do not have access to the requested workspace.'
            )

        previous_workspace_id = request.session.get('active_workspace_id')

        # Write session value.
        request.session['active_workspace_id'] = workspace_id

        # Audit row — FK references; use _id suffix so we don't hit DB for
        # workspace/user objects unnecessarily.
        WorkspaceSwitchEvent.objects.create(
            user=request.user,
            from_workspace_id=previous_workspace_id,
            to_workspace_id=workspace_id,
        )

        return redirect(reverse('admin:index'))
