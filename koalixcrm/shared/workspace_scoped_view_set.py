# -*- coding: utf-8 -*-
"""
Shared mixin to make a DRF ViewSet workspace-aware.

Resolves the active workspace in this order:
  1. WorkspaceContextMiddleware (cookie-session admin/UI requests).
  2. The ``<workspace_id>`` URL kwarg (REST API path).
  3. Default Workspace fallback for superuser sessions.

Inheriting ViewSets get:
  * ``get_queryset()`` filtered to the active workspace
    (non-superusers; superusers see everything).
  * ``perform_create()`` that stamps ``workspace`` so serializer ``create()``
    methods can pick it up via ``validated_data``.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.serializers import BaseSerializer

    from koalixcrm.core.models.workspace import Workspace


class WorkspaceScopedViewSetMixin:
    """Mixin for ViewSets backing WorkspaceScopedModel resources."""

    def _resolve_workspace(self) -> Workspace | None:
        from koalixcrm.core.models.workspace import Workspace

        active = getattr(self.request, 'active_workspace', None)
        if active is not None:
            return active

        ws_id = self.kwargs.get('workspace_id') if hasattr(self, 'kwargs') else None
        if ws_id is not None:
            ws = Workspace.objects.filter(pk=ws_id, is_active=True).first()
            if ws is not None:
                return ws

        if getattr(self.request.user, 'is_superuser', False):
            ws, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
            return ws
        return None

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        active = self._resolve_workspace()
        if active is not None:
            return qs.filter(workspace=active)
        return qs.none()

    def perform_create(self, serializer: BaseSerializer) -> None:
        active = self._resolve_workspace()
        serializer.save(workspace=active)
