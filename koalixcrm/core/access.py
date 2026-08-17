# -*- coding: utf-8 -*-
"""
Access-control helper functions for the CR-8 workspace-level grant substrate.

CR-8 §8.5 — effective_roles(), permissions_for_role(), user_workspaces().
REQ-0028 — roles_in_workspace() and is_unrestricted_actor(): the canonical
resolution point for a caller-supplied ``workspace_id`` and the single
predicate for actors exempt from the role check.

Object-level grants (visible_object_ids / RoleOnObject) are deferred to CR-10.
Role-narrowed model permissions (org ADR-0013 layer 2) are koalixcrm#429.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser
    from django.db.models import QuerySet


def _is_m2m_microservice_account(user: AbstractBaseUser) -> bool:
    """Identify the non-interactive service account by group membership.

    The group is named by ``settings.M2M_MICROSERVICE_GROUP_NAME`` and is
    administered by hand in each environment, never created by code. If the
    setting is unset, or names a group that does not exist in this database,
    nobody is a member and this returns False — without raising (REQ-0028
    AC-8).

    Deliberately *not* keyed on ``is_superuser`` (the service account carries
    ``is_superuser = False``) and deliberately not keyed on the M2M
    auto-provisioning path in ``koalixcrm/auth/m2m_authentication.py``, which
    creates a user from a ``client_id`` claim alone: a token is enough to be
    provisioned, so provisioning must not by itself confer cross-workspace
    reach.
    """
    from django.conf import settings

    group_name = getattr(settings, 'M2M_MICROSERVICE_GROUP_NAME', None)
    if not group_name:
        return False

    return user.groups.filter(name=group_name).exists()


def is_unrestricted_actor(user: AbstractBaseUser | None) -> bool:
    """Return True for actors that are not confined to the workspaces they hold a role in.

    Two of them: Django superusers, and the non-interactive service account of
    our own microservices. They are the same answer to every "may this actor
    look past their own role grants" question, so both conditions live here
    rather than being spelled ``user.is_superuser`` at each call site.

    This says nothing about *which rows* the actor may see: the workspace
    object filter still applies to them, and the effective data space is still
    exactly the URL workspace (REQ-0028 AC-9). It only answers whether the
    role check of the URL-authorization layer applies.
    """
    if user is None or not getattr(user, 'is_authenticated', False):
        return False

    return bool(user.is_superuser) or _is_m2m_microservice_account(user)


def roles_in_workspace(user: AbstractBaseUser | None, workspace_id: Any) -> set[str]:
    """Return the set of Role codes this user holds in the workspace ``workspace_id``.

    The single canonical resolution point for a URL-supplied workspace id
    (REQ-0028 AC-5): no viewset and no module-local helper queries
    ``RoleInWorkspace`` on its own.

    An empty set means "no access". It is returned for an unauthenticated
    caller, for a missing/unparseable ``workspace_id``, and — for *every*
    caller, unrestricted actors included — for a workspace that does not exist
    or is not active (AC-2, AC-7). Passing the unrestricted-actor branch
    therefore does not widen the set of reachable workspaces beyond the active
    ones, which keeps this consistent with :func:`user_workspaces`.
    """
    from koalixcrm.core.models.access import Role, RoleInWorkspace
    from koalixcrm.core.models.workspace import Workspace

    if user is None or not getattr(user, 'is_authenticated', False):
        return set()

    if workspace_id is None or workspace_id == '':
        return set()

    # `RoleInWorkspace` does not inherit `WorkspaceScopedModel` today, so its
    # manager is not workspace-aware and this escape is currently a no-op. It
    # is here because the failure it prevents would be silent if that ever
    # changed: this function is asked about a workspace the caller named, and
    # the ambient scope (set from the session by WorkspaceContextMiddleware)
    # could then only narrow that answer, never correct it — a user with roles
    # in two workspaces would resolve to no roles in every workspace but the
    # ambient one, and the membership guard would turn that into a 403.
    from koalixcrm.core.managers.workspace_aware import all_workspaces

    def _in_active_workspace() -> bool:
        """The unrestricted-actor exemption, bound to an *active* tenant.

        The exemption is from the role check, not from the existence of the
        workspace, so a missing or deactivated one still resolves to no roles.
        """
        return Workspace.objects.filter(pk=workspace_id, is_active=True).exists()

    try:
        with all_workspaces():
            # Ordered for one query on the two paths that get served: a
            # superuser costs the existence check, a role holder costs the
            # join. The group lookup behind `_is_m2m_microservice_account` is
            # reached only by callers who hold no role here — who are, except
            # for the service account itself, on their way to a 403 anyway.
            if user.is_superuser:
                return set(Role.values) if _in_active_workspace() else set()

            roles = set(
                RoleInWorkspace.objects.filter(
                    group__in=user.groups.all(),
                    workspace_id=workspace_id,
                    workspace__is_active=True,
                ).values_list('role', flat=True)
            )
            if roles:
                return roles

            if _is_m2m_microservice_account(user):
                return set(Role.values) if _in_active_workspace() else set()

            return set()
    except (TypeError, ValueError):
        # A `workspace_id` the database cannot compare against the pk column.
        # Fail closed rather than propagate a 500.
        return set()


def effective_roles(user: AbstractBaseUser | None, obj: Any) -> set[str]:
    """Return the set of Role codes this user holds on ``obj``.

    Returns workspace-level grants only (via ``obj.workspace``). The safety
    guard for objects without a ``.workspace`` attribute is preserved so that
    un-scoped models (pre-CR-9) don't raise.

    Delegates to :func:`roles_in_workspace` so there is exactly one place that
    queries ``RoleInWorkspace``.

    CR-8 §8.5.
    """
    # obj.workspace may not exist if CR-9 scoping hasn't been applied yet
    # (schema-only phase).  Guard gracefully.
    workspace = getattr(obj, 'workspace', None)
    if workspace is None:
        return set()

    return roles_in_workspace(user, workspace.pk)


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

    if is_unrestricted_actor(user):
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
