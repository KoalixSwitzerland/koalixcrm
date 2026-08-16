# -*- coding: utf-8 -*-
"""
StockMovementViewSet for koalixcrm stock (ADR-0011). Read-only for
list/retrieve; `create()` is the single dedicated posting endpoint and
routes through `services/movement_posting.post_movement` (never a generic
`ModelSerializer.save()`). `update`/`partial_update`/`destroy` are refused
(HTTP 405) — the log is immutable and append-only.
"""
from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.stock_movement import StockMovement
from koalixcrm.stock.serializers.stock_movement_serializer import (
    StockMovementJSONSerializer,
    StockMovementPostSerializer,
)
from koalixcrm.stock.services.movement_posting import post_movement


class StockMovementViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = StockMovementJSONSerializer
    queryset = StockMovement.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return StockMovementPostSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workspace = self._resolve_workspace()
        try:
            movement = post_movement(
                workspace=workspace,
                created_by=request.user if request.user.is_authenticated else None,
                **serializer.validated_data,
            )
        except DjangoValidationError as exc:
            detail = exc.message_dict if hasattr(exc, "message_dict") else exc.messages
            return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)

        output = StockMovementJSONSerializer(movement, context=self.get_serializer_context())
        return Response(output.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT/PATCH — StockMovement rows are immutable.")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT/PATCH — StockMovement rows are immutable.")

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE — StockMovement rows are append-only.")
