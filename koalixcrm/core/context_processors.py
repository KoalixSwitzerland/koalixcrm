# -*- coding: utf-8 -*-
"""
Template context processor: injects active workspace info into every request.

CR-9 §9.6.
"""

from koalixcrm.core.access import user_workspaces


def workspace_context(request):
    active = getattr(request, 'active_workspace', None)
    workspaces = []
    if getattr(request, 'user', None) and request.user.is_authenticated:
        workspaces = list(user_workspaces(request.user))
    return {
        'active_workspace': active,
        'active_workspace_color': active.color if active else '',
        'user_workspaces': workspaces,
    }
