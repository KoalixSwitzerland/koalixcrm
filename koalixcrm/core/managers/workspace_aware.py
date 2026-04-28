# -*- coding: utf-8 -*-
"""
WorkspaceAwareManager and context helpers.

CR-9 §9.2.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Iterator

from django.db import models

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser
    from django.db.models import QuerySet

    from koalixcrm.core.models.workspace import Workspace

_active_workspace: ContextVar['Workspace | None'] = ContextVar(
    '_active_workspace', default=None
)


class WorkspaceContextMissing(Exception):
    """Raised by WorkspaceAwareManager when raise_on_missing_context=True and no workspace is active."""


def activate_workspace(ws: 'Workspace') -> None:
    _active_workspace.set(ws)


def deactivate_workspace() -> None:
    _active_workspace.set(None)


def get_active_workspace() -> 'Workspace | None':
    return _active_workspace.get()


@contextmanager
def workspace_context(ws: 'Workspace') -> Iterator['Workspace']:
    token = _active_workspace.set(ws)
    try:
        yield ws
    finally:
        _active_workspace.reset(token)


class WorkspaceAwareManager(models.Manager):
    raise_on_missing_context: bool = False

    def get_queryset(self) -> 'QuerySet':
        qs = super().get_queryset()
        active = _active_workspace.get()
        if active is not None:
            return qs.filter(workspace=active)
        if self.raise_on_missing_context:
            raise WorkspaceContextMissing(
                "No active workspace set. Use activate_workspace() or workspace_context()."
            )
        return qs

    def visible_to(self, user: 'AbstractBaseUser') -> 'QuerySet':
        from koalixcrm.core.access import user_workspaces
        return self.filter(workspace__in=user_workspaces(user))
