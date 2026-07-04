# -*- coding: utf-8 -*-
"""ADR-0014: `ProductionOrder` ModelViewSet plus workflow actions
(`release`, `start`, `pick_components`, `complete`, `cancel`), all routed
through `services/production_order_workflow.py`."""
from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.production_order import ProductionOrder
from koalixcrm.stock.serializers.production_order_serializer import ProductionOrderJSONSerializer
from koalixcrm.stock.services import production_order_workflow


class ProductionOrderViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = ProductionOrderJSONSerializer
    queryset = ProductionOrder.objects.all()

    @action(detail=True, methods=['post'])
    def release(self, request, pk=None):
        production_order = self.get_object()
        try:
            production_order_workflow.release(production_order)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(production_order).data)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        production_order = self.get_object()
        try:
            production_order_workflow.start(production_order)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(production_order).data)

    @action(detail=True, methods=['post'], url_path='pick-components')
    def pick_components(self, request, pk=None):
        from koalixcrm.stock.models.location import Location

        production_order = self.get_object()
        source_location_id = request.data.get('source_location')
        if source_location_id is None:
            return Response({"detail": "source_location is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            source_location = Location.objects.get(pk=source_location_id)
            production_order_workflow.pick_components(
                production_order, source_location=source_location, created_by=request.user,
            )
        except Location.DoesNotExist:
            return Response({"detail": "source_location not found."}, status=status.HTTP_400_BAD_REQUEST)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(production_order).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        from koalixcrm.products.models.product_variant import ProductVariant
        from koalixcrm.stock.models.batch import Batch
        from koalixcrm.stock.models.location import Location
        from koalixcrm.stock.models.serial_unit import SerialUnit

        production_order = self.get_object()
        destination_location_id = request.data.get('destination_location')
        finished_variant_id = request.data.get('finished_variant')
        if destination_location_id is None or finished_variant_id is None:
            return Response(
                {"detail": "destination_location and finished_variant are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            destination_location = Location.objects.get(pk=destination_location_id)
            finished_variant = ProductVariant.objects.get(pk=finished_variant_id)
            finished_serial_unit_id = request.data.get('finished_serial_unit')
            finished_batch_id = request.data.get('finished_batch')
            finished_serial_unit = (
                SerialUnit.objects.get(pk=finished_serial_unit_id) if finished_serial_unit_id else None
            )
            finished_batch = Batch.objects.get(pk=finished_batch_id) if finished_batch_id else None
            production_order_workflow.complete(
                production_order,
                destination_location=destination_location,
                finished_variant=finished_variant,
                finished_serial_unit=finished_serial_unit,
                finished_batch=finished_batch,
                created_by=request.user,
            )
        except (Location.DoesNotExist, ProductVariant.DoesNotExist,
                SerialUnit.DoesNotExist, Batch.DoesNotExist) as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(production_order).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        production_order = self.get_object()
        try:
            production_order_workflow.cancel(production_order)
        except DjangoValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(production_order).data)
