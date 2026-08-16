# -*- coding: utf-8 -*-
"""
Stock API entry point.

Exposes Stock REST viewsets for URL routing.
"""
from __future__ import annotations

from koalixcrm.stock.views.batch_view_set import BatchViewSet
from koalixcrm.stock.views.bill_of_materials_explosion_view_set import (
    BillOfMaterialsExplosionViewSet,
)
from koalixcrm.stock.views.goods_receipt_view_set import GoodsReceiptViewSet
from koalixcrm.stock.views.handling_unit_view_set import HandlingUnitViewSet
from koalixcrm.stock.views.location_view_set import LocationViewSet
from koalixcrm.stock.views.movement_reason_code_view_set import MovementReasonCodeViewSet
from koalixcrm.stock.views.on_hand_record_view_set import OnHandRecordViewSet
from koalixcrm.stock.views.production_order_view_set import ProductionOrderViewSet
from koalixcrm.stock.views.rental_assignment_view_set import RentalAssignmentViewSet
from koalixcrm.stock.views.retention_policy_view_set import RetentionPolicyViewSet
from koalixcrm.stock.views.scan_resolve_view import ScanResolveView
from koalixcrm.stock.views.serial_unit_availability_view import SerialUnitAvailabilityView
from koalixcrm.stock.views.serial_unit_view_set import SerialUnitViewSet
from koalixcrm.stock.views.stock_balance_view_set import StockBalanceViewSet
from koalixcrm.stock.views.stock_movement_view_set import StockMovementViewSet
from koalixcrm.stock.views.stock_reservation_view_set import StockReservationViewSet

__all__ = [
    "BatchViewSet",
    "BillOfMaterialsExplosionViewSet",
    "GoodsReceiptViewSet",
    "HandlingUnitViewSet",
    "LocationViewSet",
    "MovementReasonCodeViewSet",
    "OnHandRecordViewSet",
    "ProductionOrderViewSet",
    "RentalAssignmentViewSet",
    "RetentionPolicyViewSet",
    "ScanResolveView",
    "SerialUnitAvailabilityView",
    "SerialUnitViewSet",
    "StockBalanceViewSet",
    "StockMovementViewSet",
    "StockReservationViewSet",
]
