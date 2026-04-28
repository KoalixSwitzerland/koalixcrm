# -*- coding: utf-8 -*-
"""
Template context processor: injects active workspace info into every request.

CR-9 §9.6.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.core.access import user_workspaces

if TYPE_CHECKING:
    from django.http import HttpRequest


def workspace_context(request: HttpRequest) -> dict[str, Any]:
    active = getattr(request, 'active_workspace', None)
    workspaces = []
    if getattr(request, 'user', None) and request.user.is_authenticated:
        workspaces = list(user_workspaces(request.user))
    return {
        'active_workspace': active,
        'active_workspace_color': active.color if active else '',
        'user_workspaces': workspaces,
    }
