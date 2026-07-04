# -*- coding: utf-8 -*-
"""ADR-0014: read-only `BillOfMaterialsExplosion` ViewSet plus a
`recompute` action that calls `services/bom_explosion.explode()`
synchronously (the Celery task in `koalixcrm/stock/tasks.py` is an
optional async entry point, not used by this endpoint)."""
from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.bill_of_materials_explosion import BillOfMaterialsExplosion
from koalixcrm.stock.serializers.bill_of_materials_explosion_serializer import (
    BillOfMaterialsExplosionJSONSerializer,
)


class BillOfMaterialsExplosionViewSet(WorkspaceScopedViewSetMixin,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      viewsets.GenericViewSet):
    serializer_class = BillOfMaterialsExplosionJSONSerializer
    queryset = BillOfMaterialsExplosion.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='recompute')
    def recompute(self, request):
        from koalixcrm.products.models.bill_of_materials import BillOfMaterials
        from koalixcrm.stock.services.bom_explosion import ExplosionDepthExceeded, explode

        bill_of_materials_id = request.data.get('bill_of_materials')
        if bill_of_materials_id is None:
            return Response({"detail": "bill_of_materials is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            bill_of_materials = BillOfMaterials.objects.get(pk=bill_of_materials_id)
            result = explode(bill_of_materials)
        except BillOfMaterials.DoesNotExist:
            return Response({"detail": "BillOfMaterials not found."}, status=status.HTTP_404_NOT_FOUND)
        except (ExplosionDepthExceeded, DjangoValidationError) as exc:
            return Response({"detail": exc.messages if hasattr(exc, 'messages') else str(exc)},
                            status=status.HTTP_400_BAD_REQUEST)
        rows = BillOfMaterialsExplosion.objects.filter(bill_of_materials=bill_of_materials)
        return Response({
            "depth_warning": result.depth_warning,
            "max_depth": result.max_depth,
            "rows": BillOfMaterialsExplosionJSONSerializer(rows, many=True).data,
        })
