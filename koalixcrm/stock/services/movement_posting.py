# -*- coding: utf-8 -*-
"""ADR-0011: the *only* authorized write path for `StockMovement` +
synchronous `OnHandRecord`/`StockBalance` projection updates. Every
quantity movement (`qty is not None`) is posted, in one DB transaction,
alongside its physical/aggregate effects — except `business_step =
inventorying` (Amendment 2026-05-04, OQ-0017), which is a verification-only
event that never mutates a balance; a discrepancy is posted as a *second*,
separate `adjustment` StockMovement (`post_inventory_count`).

ADR-0013 owner segregation: `OnHandRecord` always reflects physical
presence regardless of ownership, but `StockBalance` (the ATP-relevant
aggregate) is only mutated for `owner_type = OWN` rows — rental
(`RENTAL`) and foreign-owned (`CUSTOMER_CONSIGNMENT`/`CUSTOMER_OWNED`)
stock must not inflate the tenant's own ATP (ADR-0013 "geht nicht in ATP
ein").

Deferred to a later stage (see Stage 5 report): all four non-on-hand ATP
segments — `qty_booked`, `qty_reserved_for_document`, `qty_ordered` and
`qty_in_transit` — are currently unimplemented placeholders that no code
path mutates. `qty_ordered`/`qty_in_transit` need purchase-order/shipping
documents (dedicated ADR pending); `qty_booked`/`qty_reserved_for_document`
await a decision on whether reservation transitions mutate the balance
directly or emit log events (`StockReservation` rows themselves are fully
maintained by `services/reservation_lifecycle.py`).

Justification: transactional integrity — the sole authorized StockMovement write path; every posting updates OnHandRecord/StockBalance synchronously in one DB transaction (ADR-0011); still needed with the microservice fleet deleted. (Tier-2 GRANTED by architect.)
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext as _

from koalixcrm.stock.models.choices import BusinessStep, OwnerType

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from django.db.models import Model

    from koalixcrm.core.models.workspace import Workspace
    from koalixcrm.products.models.product_variant import ProductVariant
    from koalixcrm.stock.models.batch import Batch
    from koalixcrm.stock.models.handling_unit import HandlingUnit
    from koalixcrm.stock.models.location import Location
    from koalixcrm.stock.models.movement_reason_code import MovementReasonCode
    from koalixcrm.stock.models.serial_unit import SerialUnit
    from koalixcrm.stock.models.stock_movement import StockMovement


@dataclass(frozen=True)
class OnHandDelta:
    """A single, pure (no-DB-write) intended change to one `OnHandRecord`
    key, produced by `_compute_deltas`. `counts_toward_balance` mirrors the
    ADR-0013 owner-segregation rule: only `OwnerType.OWN` deltas also apply
    to the `StockBalance.qty_on_hand` aggregate."""

    location: "Location"
    owner_type: str
    owner_party: Any
    delta: Decimal
    counts_toward_balance: bool

    @property
    def location_id(self):
        return self.location.pk

    @property
    def owner_party_id(self):
        return self.owner_party.pk if self.owner_party is not None else None


def _compute_deltas(movement: "StockMovement") -> list[OnHandDelta]:
    """Pure function: given a (not-yet-persisted-or-not) StockMovement,
    return the list of intended OnHandRecord/StockBalance deltas. Used both
    by `_apply_deltas` (live posting) and `rebuild_from_log` (replay)."""
    if movement.qty is None or movement.business_step == BusinessStep.INVENTORYING:
        return []

    qty = movement.qty
    source = movement.source_location
    destination = movement.destination_location
    own = movement.owner_type == OwnerType.OWN

    if movement.business_step == BusinessStep.ADJUSTMENT:
        loc = destination or source
        if loc is None:
            raise ValidationError(
                _("business_step=adjustment requires source_location or destination_location.")
            )
        return [OnHandDelta(loc, movement.owner_type, movement.owner_party, qty, own)]

    if movement.business_step == BusinessStep.RENTAL_OUT:
        deltas: list[OnHandDelta] = []
        if source is not None:
            deltas.append(OnHandDelta(source, OwnerType.OWN, None, -qty, True))
        if destination is not None:
            deltas.append(OnHandDelta(destination, movement.owner_type, movement.owner_party, qty, own))
        return deltas

    if movement.business_step == BusinessStep.RENTAL_RETURN:
        deltas = []
        if source is not None:
            deltas.append(OnHandDelta(source, OwnerType.RENTAL, movement.owner_party, -qty, False))
        if destination is not None:
            deltas.append(OnHandDelta(destination, OwnerType.OWN, None, qty, True))
        return deltas

    if source is None and destination is None:
        raise ValidationError(
            _("A quantity movement requires source_location and/or destination_location.")
        )

    deltas = []
    if source is not None:
        deltas.append(OnHandDelta(source, movement.owner_type, movement.owner_party, -qty, own))
    if destination is not None:
        deltas.append(OnHandDelta(destination, movement.owner_type, movement.owner_party, qty, own))
    # ACCEPTING: on_hand at destination increases by the generic delta above;
    # the corresponding qty_quarantine release at the same location is applied
    # separately in `_apply_balance_delta` via `_quarantine_release_delta` — it
    # is a StockBalance-only bookkeeping move (quarantine bucket -> free stock),
    # not a second OnHandRecord delta.
    return deltas


def _quarantine_release_delta(movement: "StockMovement") -> Decimal:
    """`accepting` releases `qty` from `StockBalance.qty_quarantine` at the
    destination, in addition to the on_hand deltas from `_compute_deltas`."""
    if (movement.business_step == BusinessStep.ACCEPTING
            and movement.qty is not None
            and movement.destination_location is not None
            and movement.owner_type == OwnerType.OWN):
        return movement.qty
    return Decimal("0")


def _get_or_create_on_hand_record(
    *,
    workspace: "Workspace",
    variant: "ProductVariant",
    location: "Location",
    batch: "Batch | None",
    serial_unit: "SerialUnit | None",
    owner_type: str,
    owner_party,
    uom,
):
    from koalixcrm.stock.models.on_hand_record import OnHandRecord

    record, _created = OnHandRecord.objects.select_for_update().get_or_create(
        workspace=workspace,
        variant=variant,
        location=location,
        batch=batch,
        serial_unit=serial_unit,
        owner_type=owner_type,
        owner_party=owner_party,
        defaults={"qty_on_hand": Decimal("0"), "uom": uom},
    )
    return record


def _apply_on_hand_delta(movement: "StockMovement", item: OnHandDelta) -> None:
    from koalixcrm.stock.models.on_hand_record import OnHandRecord

    record = _get_or_create_on_hand_record(
        workspace=movement.workspace,
        variant=movement.variant,
        location=item.location,
        batch=movement.batch,
        serial_unit=movement.serial_unit,
        owner_type=item.owner_type,
        owner_party=item.owner_party,
        uom=movement.uom,
    )
    new_qty = record.qty_on_hand + item.delta
    if new_qty < Decimal("0"):
        raise ValidationError(
            _("Movement would drive OnHandRecord qty_on_hand negative at location %(loc)s.")
            % {"loc": item.location_id}
        )
    if movement.serial_unit_id is not None and new_qty == Decimal("0"):
        if record.pk is not None:
            record.delete()
        return
    record.qty_on_hand = new_qty
    record.full_clean()
    record.save()


def _apply_balance_delta(movement: "StockMovement", item: OnHandDelta) -> None:
    if not item.counts_toward_balance:
        return
    from koalixcrm.stock.models.stock_balance import StockBalance

    balance, _created = StockBalance.objects.select_for_update().get_or_create(
        workspace=movement.workspace,
        variant=movement.variant,
        location=item.location,
        defaults={"uom": movement.uom},
    )
    new_on_hand = balance.qty_on_hand + item.delta
    if new_on_hand < Decimal("0"):
        raise ValidationError(
            _("Movement would drive StockBalance qty_on_hand negative at location %(loc)s.")
            % {"loc": item.location}
        )
    balance.qty_on_hand = new_on_hand
    balance.full_clean()
    balance.save()

    quarantine_release = _quarantine_release_delta(movement)
    if quarantine_release and item.location_id == movement.destination_location_id and item.delta < Decimal("0"):
        new_quarantine = balance.qty_quarantine - quarantine_release
        if new_quarantine < Decimal("0"):
            raise ValidationError(
                _("Movement would drive StockBalance qty_quarantine negative at location %(loc)s.")
                % {"loc": item.location}
            )
        balance.qty_quarantine = new_quarantine
        balance.full_clean()
        balance.save()


def post_movement(
    *,
    workspace: "Workspace",
    event_type: str,
    business_step: str,
    occurred_at,
    variant: "ProductVariant",
    product=None,
    source_location: "Location | None" = None,
    destination_location: "Location | None" = None,
    batch: "Batch | None" = None,
    serial_unit: "SerialUnit | None" = None,
    handling_unit: "HandlingUnit | None" = None,
    parent_serial_unit: "SerialUnit | None" = None,
    parent_batch: "Batch | None" = None,
    aggregation_group=None,
    qty: Decimal | None = None,
    uom=None,
    reason_code: "MovementReasonCode | None" = None,
    document: "Model | None" = None,
    document_type=None,
    document_id: int | None = None,
    owner_type: str = OwnerType.OWN,
    owner_party=None,
    disposition: str | None = None,
    idempotency_key: uuid.UUID | None = None,
    compensates: "StockMovement | None" = None,
    created_by: "User | None" = None,
) -> "StockMovement":
    """Post one `StockMovement` and, in the same DB transaction, apply its
    `OnHandRecord`/`StockBalance` effects (ADR-0011). Idempotent on
    `idempotency_key`: a retried request with the same key returns the
    already-posted row instead of creating a duplicate. The generic
    document reference can be passed either as a model instance
    (`document=`) or as an already-resolved `(document_type, document_id)`
    pair (e.g. from an admin form)."""
    from django.contrib.contenttypes.models import ContentType

    from koalixcrm.stock.models.stock_movement import StockMovement

    idempotency_key = idempotency_key or uuid.uuid4()

    existing = StockMovement.objects.filter(workspace=workspace, idempotency_key=idempotency_key).first()
    if existing is not None:
        return existing

    product = product or variant.product
    if document is not None:
        document_type = ContentType.objects.get_for_model(document)
        document_id = document.pk

    with transaction.atomic():
        movement = StockMovement(
            workspace=workspace,
            event_type=event_type,
            business_step=business_step,
            occurred_at=occurred_at,
            source_location=source_location,
            destination_location=destination_location,
            product=product,
            variant=variant,
            batch=batch,
            serial_unit=serial_unit,
            handling_unit=handling_unit,
            parent_serial_unit=parent_serial_unit,
            parent_batch=parent_batch,
            aggregation_group=aggregation_group,
            qty=qty,
            uom=uom,
            reason_code=reason_code,
            document_type=document_type,
            document_id=document_id,
            owner_type=owner_type,
            owner_party=owner_party,
            disposition=disposition,
            idempotency_key=idempotency_key,
            compensates=compensates,
            created_by=created_by,
        )
        movement.full_clean()
        movement.save()

        for item in _compute_deltas(movement):
            _apply_on_hand_delta(movement, item)
            _apply_balance_delta(movement, item)

    return movement


def post_inventory_count(
    *,
    workspace: "Workspace",
    variant: "ProductVariant",
    location: "Location",
    counted_qty: Decimal,
    occurred_at,
    uom,
    owner_type: str = OwnerType.OWN,
    owner_party=None,
    batch: "Batch | None" = None,
    serial_unit: "SerialUnit | None" = None,
    created_by: "User | None" = None,
    reason_code_discrepancy: "MovementReasonCode | None" = None,
) -> tuple["StockMovement", "StockMovement | None"]:
    """UC-0008/UC-0009 ad-hoc cycle count. Always posts the `inventorying`
    verification event (no balance mutation, Amendment OQ-0017). If
    `counted_qty` differs from the current `OnHandRecord.qty_on_hand`, also
    posts a second, separate `adjustment` movement carrying the delta
    (the only record of the two that mutates OnHandRecord/StockBalance)."""
    from koalixcrm.stock.models.choices import BusinessStep, EventType
    from koalixcrm.stock.models.on_hand_record import OnHandRecord

    inventorying_movement = post_movement(
        workspace=workspace,
        event_type=EventType.OBJECT_EVENT,
        business_step=BusinessStep.INVENTORYING,
        occurred_at=occurred_at,
        variant=variant,
        destination_location=location,
        qty=None,
        uom=uom,
        owner_type=owner_type,
        owner_party=owner_party,
        batch=batch,
        serial_unit=serial_unit,
        created_by=created_by,
    )

    current = OnHandRecord.objects.filter(
        workspace=workspace,
        variant=variant,
        location=location,
        batch=batch,
        serial_unit=serial_unit,
        owner_type=owner_type,
        owner_party=owner_party,
    ).first()
    current_qty = current.qty_on_hand if current is not None else Decimal("0")
    delta = counted_qty - current_qty

    if delta == Decimal("0"):
        return inventorying_movement, None

    adjustment_movement = post_movement(
        workspace=workspace,
        event_type=EventType.OBJECT_EVENT,
        business_step=BusinessStep.ADJUSTMENT,
        occurred_at=occurred_at,
        variant=variant,
        destination_location=location if delta > 0 else None,
        source_location=location if delta < 0 else None,
        qty=abs(delta) if delta > 0 else delta,
        uom=uom,
        owner_type=owner_type,
        owner_party=owner_party,
        batch=batch,
        serial_unit=serial_unit,
        reason_code=reason_code_discrepancy,
        created_by=created_by,
    )
    return inventorying_movement, adjustment_movement


def rebuild_from_log(*, workspace: "Workspace") -> dict:
    """REQ-0019 AC-3: recompute `OnHandRecord`/`StockBalance` totals purely
    from the immutable `StockMovement` log (replaying `_compute_deltas` in
    `recorded_at` order) and compare against the stored aggregates. Returns
    a report dict; never writes anything (read-only consistency check)."""
    from koalixcrm.stock.models.on_hand_record import OnHandRecord
    from koalixcrm.stock.models.stock_balance import StockBalance
    from koalixcrm.stock.models.stock_movement import StockMovement

    on_hand_totals: dict[tuple, Decimal] = {}
    balance_totals: dict[tuple, Decimal] = {}

    movements = StockMovement.objects.filter(workspace=workspace).order_by("recorded_at", "id")
    for movement in movements:
        for item in _compute_deltas(movement):
            key = (movement.variant_id, item.location_id, movement.batch_id,
                   movement.serial_unit_id, item.owner_type, item.owner_party_id)
            on_hand_totals[key] = on_hand_totals.get(key, Decimal("0")) + item.delta
            if item.counts_toward_balance:
                bkey = (movement.variant_id, item.location_id)
                balance_totals[bkey] = balance_totals.get(bkey, Decimal("0")) + item.delta

    on_hand_mismatches = []
    seen_keys = set()
    for record in OnHandRecord.objects.filter(workspace=workspace):
        key = (record.variant_id, record.location_id, record.batch_id,
               record.serial_unit_id, record.owner_type, record.owner_party_id)
        seen_keys.add(key)
        expected = on_hand_totals.get(key, Decimal("0"))
        if expected != record.qty_on_hand:
            on_hand_mismatches.append({
                "key": key, "stored": record.qty_on_hand, "expected": expected,
            })
    for key, expected in on_hand_totals.items():
        if key not in seen_keys and expected != Decimal("0"):
            on_hand_mismatches.append({"key": key, "stored": Decimal("0"), "expected": expected})

    balance_mismatches = []
    seen_bkeys = set()
    for balance in StockBalance.objects.filter(workspace=workspace):
        bkey = (balance.variant_id, balance.location_id)
        seen_bkeys.add(bkey)
        expected = balance_totals.get(bkey, Decimal("0"))
        if expected != balance.qty_on_hand:
            balance_mismatches.append({
                "key": bkey, "stored": balance.qty_on_hand, "expected": expected,
            })
    for bkey, expected in balance_totals.items():
        if bkey not in seen_bkeys and expected != Decimal("0"):
            balance_mismatches.append({"key": bkey, "stored": Decimal("0"), "expected": expected})

    return {
        "consistent": not on_hand_mismatches and not balance_mismatches,
        "on_hand_mismatches": on_hand_mismatches,
        "balance_mismatches": balance_mismatches,
    }
