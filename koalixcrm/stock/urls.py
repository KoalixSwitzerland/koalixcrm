"""Per-app REST API routes for koalixcrm Stock (ADR-0009/ADR-0012 backbone;
ADR-0010/ADR-0011/ADR-0013 Stage 5 stock states/movements/rental;
ADR-0014/ADR-0015/ADR-0016/ADR-0017 Stage 6 assembly/lifecycle/scan/goods-receipt).

Mounted at ``/koalixcrm_stock/api/v1/<workspace_id>/`` from
``projectsettings/urls.py``, mirroring the products/contacts app wiring
(CR-002).
"""
from __future__ import annotations

from django.urls import path
from rest_framework.routers import DefaultRouter

from koalixcrm.stock_api_py.stock_api import (
    BatchViewSet,
    BillOfMaterialsExplosionViewSet,
    GoodsReceiptViewSet,
    HandlingUnitViewSet,
    LocationViewSet,
    MovementReasonCodeViewSet,
    OnHandRecordViewSet,
    ProductionOrderViewSet,
    RentalAssignmentViewSet,
    RetentionPolicyViewSet,
    ScanResolveView,
    SerialUnitAvailabilityView,
    SerialUnitViewSet,
    StockBalanceViewSet,
    StockMovementViewSet,
    StockReservationViewSet,
)

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'handling-units', HandlingUnitViewSet, basename='handling-unit')
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'serial-units', SerialUnitViewSet, basename='serial-unit')
router.register(r'on-hand-records', OnHandRecordViewSet, basename='on-hand-record')
router.register(r'retention-policies', RetentionPolicyViewSet, basename='retention-policy')
router.register(r'movement-reason-codes', MovementReasonCodeViewSet, basename='movement-reason-code')
router.register(r'stock-movements', StockMovementViewSet, basename='stock-movement')
router.register(r'stock-balances', StockBalanceViewSet, basename='stock-balance')
router.register(r'stock-reservations', StockReservationViewSet, basename='stock-reservation')
router.register(r'rental-assignments', RentalAssignmentViewSet, basename='rental-assignment')
router.register(r'goods-receipts', GoodsReceiptViewSet, basename='goods-receipt')
router.register(r'production-orders', ProductionOrderViewSet, basename='production-order')
router.register(r'bom-explosions', BillOfMaterialsExplosionViewSet, basename='bom-explosion')

urlpatterns = router.urls + [
    path(
        'variants/<int:variant_id>/serial-units/availability/',
        SerialUnitAvailabilityView.as_view(),
        name='variant-serial-unit-availability',
    ),
    path(
        'scan/resolve/',
        ScanResolveView.as_view(),
        name='scan-resolve',
    ),
]
