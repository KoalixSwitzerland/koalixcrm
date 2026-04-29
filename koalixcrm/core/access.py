# -*- coding: utf-8 -*-
"""
Access-control helper functions for the CR-8 workspace-level grant substrate.

CR-8 §8.5 — effective_roles(), permissions_for_role(), user_workspaces().

Object-level grants (visible_object_ids / RoleOnObject) are deferred to CR-10.
Note: superuser bypass and request integration are CR-9 territory.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser
    from django.db.models import QuerySet


def effective_roles(user: AbstractBaseUser | None, obj: Any) -> set[str]:
    """Return the set of Role codes this user holds on ``obj``.

    Returns workspace-level grants only (via ``obj.workspace``).  The safety
    guard for objects without a ``.workspace`` attribute is preserved so that
    un-scoped models (pre-CR-9) don't raise.

    Roles are derived by traversing user → groups → RoleInWorkspace rows.

    CR-8 §8.5.
    """
    from koalixcrm.core.models.access import Role, RoleInWorkspace

    if user is None or not getattr(user, 'is_authenticated', False):
        return set()

    if user.is_superuser:
        return set(Role.values)

    # obj.workspace may not exist if CR-9 scoping hasn't been applied yet
    # (schema-only phase).  Guard gracefully.
    workspace = getattr(obj, 'workspace', None)
    if workspace is None:
        return set()

    return set(
        RoleInWorkspace.objects.filter(
            group__in=user.groups.all(),
            workspace=workspace,
        ).values_list('role', flat=True)
    )


def user_workspaces(user: AbstractBaseUser | None) -> QuerySet:
    """Return the queryset of Workspace rows the user has any role in.

    Used by the dashboard switcher and the switch view's authorisation check.
    Deactivated workspaces are excluded even if a stale role row still
    references them.

    CR-8 §8.5.
    """
    from koalixcrm.core.models.workspace import Workspace

    if user is None or not getattr(user, 'is_authenticated', False):
        return Workspace.objects.none()

    if user.is_superuser:
        return Workspace.objects.filter(is_active=True)

    return Workspace.objects.filter(
        is_active=True,
        group_role_assignments__group__in=user.groups.all(),
    ).distinct()


def permissions_for_role(role: str) -> set[str]:
    """Map a Role value to the set of Django per-model permission codes.

    Returns a subset of {'add', 'change', 'delete', 'view'}.

    Mapping (CR §9.8):
      ADMIN           → add + change + delete + view
      EDITOR          → add + change + view
      VIEWER          → view
      COMMENTER       → view  (commenting is app-specific; map to view here)
      EMPLOYEE        → view  (workflow participant; per-app code can layer in object-level perms)
      LINE_MANAGER    → add + change + view  (people-management edits, no destructive ops)
      PROJECT_MANAGER → add + change + view  (project-lead edits, no destructive ops)

    CR-8 §8.2, §9.8.
    """
    from koalixcrm.core.models.access import Role

    _map = {
        Role.ADMIN:           {'add', 'change', 'delete', 'view'},
        Role.EDITOR:          {'add', 'change', 'view'},
        Role.VIEWER:          {'view'},
        Role.COMMENTER:       {'view'},
        Role.EMPLOYEE:        {'view'},
        Role.LINE_MANAGER:    {'add', 'change', 'view'},
        Role.PROJECT_MANAGER: {'add', 'change', 'view'},
    }
    return _map.get(role, set())
