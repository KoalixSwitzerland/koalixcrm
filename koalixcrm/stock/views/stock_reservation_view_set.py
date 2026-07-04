# -*- coding: utf-8 -*-
"""
StockReservationViewSet for koalixcrm stock (ADR-0010). Fully editable
ModelViewSet plus dedicated lifecycle actions (`mark_sent`, `confirm`,
`cancel`, `fulfill`) that route through
`services/reservation_lifecycle.py`, so the first-SENT-wins concurrency
rule is enforced consistently regardless of caller.
"""
from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.stock_reservation import StockReservation
from koalixcrm.stock.serializers.stock_reservation_serializer import StockReservationJSONSerializer
from koalixcrm.stock.services import reservation_lifecycle


class StockReservationViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = StockReservationJSONSerializer
    queryset = StockReservation.objects.all()

    @action(detail=True, methods=['post'])
    def mark_sent(self, request, pk=None):
        reservation = self.get_object()
        try:
            reservation_lifecycle.mark_sent(reservation)
        except reservation_lifecycle.ReservationConflict as exc:
            return Response(
                {"detail": str(exc), "colliding_reservation_id": exc.colliding_reservation_id},
                status=status.HTTP_409_CONFLICT,
            )
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(reservation).data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        reservation = self.get_object()
        try:
            reservation_lifecycle.confirm(reservation)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(reservation).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        try:
            reservation_lifecycle.cancel(reservation)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(reservation).data)

    @action(detail=True, methods=['post'])
    def fulfill(self, request, pk=None):
        reservation = self.get_object()
        try:
            reservation_lifecycle.fulfill(reservation)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(reservation).data)
