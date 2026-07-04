# -*- coding: utf-8 -*-
"""ADR-0014 §Bestandsfluss bei Fertigungsabschluss: the `ProductionOrder`
state machine and its stock-flow side effects.

  1. `release()`      DRAFT -> RELEASED
  2. `start()`         RELEASED -> IN_PROGRESS; resolves each component's
                       ProductVariant (three-step order,
                       `services/component_variant_resolution.py`) and
                       creates a `StockReservation`
                       (`reservation_type=RESERVED_FOR_DOCUMENT`) per
                       component.
  3. `pick_components()` posts one `picking` `OBJECT_EVENT` per component,
                       consuming the reserved `OnHandRecord` quantity.
  4. `complete()`      posts one `TRANSFORMATION_EVENT` for the finished
                       good plus one or more `AGGREGATION_EVENT` rows
                       (shared `aggregation_group`) for the As-Built BOM,
                       fulfils every component's `StockReservation`, and
                       transitions the order to `COMPLETED`.

All quantity-affecting steps happen inside one DB transaction per call,
consistent with ADR-0011's synchronous-posting invariant.
"""
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from koalixcrm.products.models.choices import TrackingMode
from koalixcrm.stock.models.choices import ProductionOrderStatus, ReservationKind, ReservationType

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from koalixcrm.stock.models.production_order import ProductionOrder


def release(production_order: "ProductionOrder") -> "ProductionOrder":
    if production_order.status != ProductionOrderStatus.DRAFT:
        raise ValidationError(_("Only a DRAFT ProductionOrder can be RELEASED."))
    production_order.status = ProductionOrderStatus.RELEASED
    production_order.full_clean()
    production_order.save()
    return production_order


@transaction.atomic
def start(production_order: "ProductionOrder") -> "ProductionOrder":
    """RELEASED -> IN_PROGRESS: explodes the BOM into
    `ProductionOrderComponent` rows (if not already present), resolving
    each component's variant and reserving stock for it."""
    from koalixcrm.stock.models.production_order_component import ProductionOrderComponent
    from koalixcrm.stock.services import reservation_lifecycle
    from koalixcrm.stock.services.component_variant_resolution import resolve_component_variant

    if production_order.status != ProductionOrderStatus.RELEASED:
        raise ValidationError(_("Only a RELEASED ProductionOrder can transition to IN_PROGRESS."))

    if not production_order.components.exists():
        for bom_item in production_order.bill_of_materials.items.all():
            variant = resolve_component_variant(bom_item)
            planned_qty = bom_item.quantity * production_order.planned_qty
            if bom_item.scrap_pct:
                planned_qty = planned_qty * (1 + bom_item.scrap_pct / 100)
            component = ProductionOrderComponent(
                workspace=production_order.workspace,
                production_order=production_order,
                bom_item=bom_item,
                product=bom_item.component_product,
                variant=variant,
                planned_qty=planned_qty,
                uom=bom_item.unit,
            )
            component.full_clean()
            component.save()

    for component in production_order.components.select_related("variant").all():
        if component.reservation_id is not None:
            continue
        reservation = reservation_lifecycle.create_reservation(
            workspace=production_order.workspace,
            variant=component.variant,
            kind=ReservationKind.SALE,
            qty_reserved=component.planned_qty,
            uom=component.uom,
            document=production_order,
        )
        reservation.reservation_type = ReservationType.RESERVED_FOR_DOCUMENT
        reservation.full_clean()
        reservation.save()
        component.reservation = reservation
        component.save(update_fields=["reservation"])

    production_order.status = ProductionOrderStatus.IN_PROGRESS
    production_order.full_clean()
    production_order.save()
    return production_order


@transaction.atomic
def pick_components(production_order: "ProductionOrder", *, source_location, occurred_at=None,
                    created_by: "User | None" = None) -> "ProductionOrder":
    """Physical component entnahme: posts one `picking` `OBJECT_EVENT` per
    component, using `component.planned_qty` as `actual_qty` unless already
    set."""
    from koalixcrm.stock.models.choices import BusinessStep, EventType
    from koalixcrm.stock.services.movement_posting import post_movement

    if production_order.status != ProductionOrderStatus.IN_PROGRESS:
        raise ValidationError(_("Components can only be picked while IN_PROGRESS."))

    occurred_at = occurred_at or timezone.now()

    for component in production_order.components.select_related("variant", "batch", "uom").all():
        qty = component.actual_qty if component.actual_qty else component.planned_qty
        post_movement(
            workspace=production_order.workspace,
            event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.PICKING,
            occurred_at=occurred_at,
            variant=component.variant,
            source_location=source_location,
            batch=component.batch,
            qty=qty,
            uom=component.uom,
            document=production_order,
            created_by=created_by,
        )
        component.actual_qty = qty
        component.save(update_fields=["actual_qty"])

    return production_order


@transaction.atomic
def complete(production_order: "ProductionOrder", *, destination_location, finished_variant,
            occurred_at=None, finished_serial_unit=None, finished_batch=None,
            created_by: "User | None" = None) -> "ProductionOrder":
    """Fertigstellung: posts one `TRANSFORMATION_EVENT` for the finished
    good and one `AGGREGATION_EVENT` per component (shared
    `aggregation_group`), fulfils every component's `StockReservation`, and
    transitions to `COMPLETED`."""
    from koalixcrm.stock.models.choices import BusinessStep, EventType
    from koalixcrm.stock.services import reservation_lifecycle
    from koalixcrm.stock.services.movement_posting import post_movement

    if production_order.status != ProductionOrderStatus.IN_PROGRESS:
        raise ValidationError(_("Only an IN_PROGRESS ProductionOrder can be completed."))

    tracking_mode = finished_variant.tracking_mode
    if tracking_mode == TrackingMode.SERIAL and finished_serial_unit is None:
        raise ValidationError(_("finished_serial_unit is required when tracking_mode = SERIAL."))
    if tracking_mode == TrackingMode.BATCH and finished_batch is None:
        raise ValidationError(_("finished_batch is required when tracking_mode = BATCH."))

    occurred_at = occurred_at or timezone.now()
    aggregation_group = uuid.uuid4()

    post_movement(
        workspace=production_order.workspace,
        event_type=EventType.TRANSFORMATION_EVENT,
        business_step=BusinessStep.COMMISSIONING,
        occurred_at=occurred_at,
        variant=finished_variant,
        destination_location=destination_location,
        serial_unit=finished_serial_unit,
        batch=finished_batch,
        qty=production_order.planned_qty,
        uom=production_order.uom,
        document=production_order,
        created_by=created_by,
    )

    components = list(production_order.components.select_related("variant", "batch").all())
    for component in components:
        parent_serial_unit = finished_serial_unit if tracking_mode == TrackingMode.SERIAL else None
        parent_batch = finished_batch if tracking_mode == TrackingMode.BATCH else None
        post_movement(
            workspace=production_order.workspace,
            event_type=EventType.AGGREGATION_EVENT,
            business_step=BusinessStep.COMMISSIONING,
            occurred_at=occurred_at,
            variant=component.variant,
            batch=component.batch,
            qty=None,
            aggregation_group=aggregation_group,
            parent_serial_unit=parent_serial_unit,
            parent_batch=parent_batch,
            document=production_order,
            created_by=created_by,
        )
        if component.reservation_id is not None:
            reservation_lifecycle.fulfill(component.reservation)

    production_order.status = ProductionOrderStatus.COMPLETED
    production_order.completed_at = occurred_at
    production_order.finished_serial_unit = finished_serial_unit
    production_order.finished_batch = finished_batch
    production_order.aggregation_group = aggregation_group
    production_order.full_clean()
    production_order.save()
    return production_order


def cancel(production_order: "ProductionOrder") -> "ProductionOrder":
    from koalixcrm.stock.services import reservation_lifecycle

    if production_order.status == ProductionOrderStatus.COMPLETED:
        raise ValidationError(_("A COMPLETED ProductionOrder cannot be cancelled."))
    for component in production_order.components.all():
        if component.reservation_id is not None:
            reservation_lifecycle.cancel(component.reservation)
    production_order.status = ProductionOrderStatus.CANCELLED
    production_order.full_clean()
    production_order.save()
    return production_order
