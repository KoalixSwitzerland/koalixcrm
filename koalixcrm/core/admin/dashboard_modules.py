# -*- coding: utf-8 -*-
"""
Grappelli dashboard module: WorkspaceSwitcherModule.

Renders the list of workspaces where the current user holds any
RoleInWorkspace row, with a switch action and an active-workspace marker.

CR-8 §8.6.
"""
from __future__ import annotations

from typing import Any

from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import modules


class WorkspaceSwitcherModule(modules.DashboardModule):
    """Dashboard module that shows the user's workspaces and lets them switch.

    Place this as the *first* child in CustomIndexDashboard.init_with_context
    so the active workspace is always the first thing the user sees.

    Usage in your dashboard.py::

        from koalixcrm.core.admin.dashboard_modules import WorkspaceSwitcherModule

        class CustomIndexDashboard(Dashboard):
            def init_with_context(self, context):
                self.children.append(WorkspaceSwitcherModule(column=1))
                ...

    The module populates ``self.workspace_rows`` (consumed by its template)
    inside ``init_with_context``.  Each row is a dict with keys:
        workspace_id, name, color, roles, is_active, switch_url
    """

    title = _('Active Workspace')
    template = 'admin/dashboard/workspace_switcher.html'
    collapsible = False

    # Custom attribute populated in init_with_context
    workspace_rows = None
    no_access = False

    def init_with_context(self, context: dict[str, Any]) -> None:
        request = context['request']
        user = request.user

        # Import here to avoid module-load-time circular imports.
        from koalixcrm.core.access import user_workspaces
        from koalixcrm.core.models.access import RoleInWorkspace

        try:
            from django.urls import reverse
            switch_url = reverse('core-workspace-switch')
        except Exception:
            switch_url = '/admin/core/workspace/switch/'

        active_workspace_id = request.session.get('active_workspace_id')

        # Fetch all workspaces this user can reach via group membership.
        workspaces = user_workspaces(user).order_by('name')

        # Build one row per workspace (aggregating all roles the user holds
        # via their group memberships).
        workspace_map: dict = {}
        for ws in workspaces:
            ws_id = ws.id
            role_codes = (
                RoleInWorkspace.objects
                .filter(group__in=user.groups.all(), workspace=ws)
                .values_list('role', flat=True)
            )
            # Resolve display labels.
            role_display = []
            for code in role_codes:
                # Construct a temporary instance just to call get_role_display.
                tmp = RoleInWorkspace(role=code)
                role_display.append(tmp.get_role_display())
            workspace_map[ws_id] = {
                'workspace_id': ws_id,
                'name': ws.name,
                'color': ws.color,
                'roles': role_display,
                'is_active': (ws_id == active_workspace_id),
                'switch_url': switch_url,
            }

        self.workspace_rows = list(workspace_map.values())

        if not self.workspace_rows:
            self.no_access = True
            # Provide a placeholder child so is_empty() returns False and
            # the module renders with the "no access" message.
            self.children = [None]
        else:
            # Ensure is_empty() returns False.
            self.children = self.workspace_rows

    def is_empty(self) -> bool:
        # Always render the module so the switcher is always visible.
        return False
