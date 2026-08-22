# -*- coding: utf-8 -*-
"""
Shared mixin to make a DRF ViewSet workspace-aware.

The workspace in force is decided by ``WorkspaceContextMiddleware``, which
gives the ``<workspace_id>`` URL segment precedence over the session
(REQ-0028). This mixin only consumes that decision; it re-reads the URL kwarg
solely so it still behaves correctly when the middleware is not installed
(bare ``APIRequestFactory`` tests, embedders running a reduced stack).

There is no fallback workspace. A read must never create a tenant row, and a
substituted tenant is a wrong answer rather than a lenient one: where no
authorized workspace can be determined the answer is 403 (AC-10). Whether the
caller may reach the workspace at all is not decided here either — that is
``WorkspaceMembershipPermission``, injected centrally in ``CoreConfig.ready()``.

Inheriting ViewSets get:
  * ``get_queryset()`` filtered to that workspace — for *every* caller,
    unrestricted actors included: passing the authorization gate does not
    widen the data space (AC-9).
  * ``perform_create()`` that stamps ``workspace`` so serializer ``create()``
    methods can pick it up via ``validated_data``.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.exceptions import PermissionDenied

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

        ws_id = (getattr(self, 'kwargs', None) or {}).get('workspace_id')
        if ws_id is None:
            return None

        try:
            return Workspace.objects.filter(pk=ws_id, is_active=True).first()
        except (TypeError, ValueError):
            return None

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        active = self._resolve_workspace()
        if active is None:
            return qs.none()
        return qs.filter(workspace=active)

    def perform_create(self, serializer: BaseSerializer) -> None:
        active = self._resolve_workspace()
        if active is None:
            # Reached only if a route without a `workspace_id` kwarg mounts a
            # workspace-scoped resource; there is no tenant to attribute the
            # row to, and inventing one is what AC-10 forbids.
            raise PermissionDenied('No authorized workspace for this request.')
        serializer.save(workspace=active)
