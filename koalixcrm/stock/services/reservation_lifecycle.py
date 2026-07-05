# -*- coding: utf-8 -*-
"""ADR-0010 (Amendments OQ-0011/OQ-0012/OQ-0013) service-level
`StockReservation` state-machine transitions, incl. the offer-lifecycle ->
reservation coupling table and the first-SENT-wins concurrency rule.
Documents (offers/orders) are out of scope for the stock app (ADR-0010
generic `document_type`/`document_id` reference) — this module operates
purely on `StockReservation` rows; the caller (a future contracts/offer
service) is responsible for invoking these transitions when its own
document status changes.

Offer status -> StockReservation coupling (ADR-0010 Amendment OQ-0012):

| Offer status | reservation.status | reservation.reservation_status |
|--------------|---------------------|----------------------------------|
| DRAFT        | ACTIVE              | PROVISIONAL                      |
| SENT         | ACTIVE              | PROVISIONAL (+ sent_at stamped)  |
| ACCEPTED     | ACTIVE              | CONFIRMED                        |
| REJECTED     | CANCELLED           | -                                 |
| EXPIRED      | CANCELLED           | -                                 |
| CANCELLED    | CANCELLED           | -                                 |

Justification: transactional integrity — mark_sent()'s first-SENT-wins concurrency rule requires an atomic compare-and-set inside one DB transaction; an idempotent CRUD-over-HTTP retry cannot express first-wins semantics; still needed with the microservice fleet deleted. (Tier-2 GRANTED by architect.)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from koalixcrm.stock.models.choices import (
    BusinessStep,
    Disposition,
    EventType,
    ReservationConfirmationStatus,
    ReservationKind,
    ReservationLifecycleStatus,
)

if TYPE_CHECKING:
    from koalixcrm.stock.models.stock_reservation import StockReservation


class ReservationConflict(ValidationError):
    """Raised when a `mark_sent()` call loses the first-SENT-wins race.
    View layers should translate this to HTTP 409."""

    def __init__(self, message: str, *, colliding_reservation_id: int):
        super().__init__(message)
        self.colliding_reservation_id = colliding_reservation_id


def create_reservation(*, workspace, variant, kind, qty_reserved=None, uom=None,
                       location=None, batch=None, serial_unit=None,
                       document=None, rental_start=None, rental_end=None,
                       expires_at=None) -> "StockReservation":
    """DRAFT-equivalent: create a PROVISIONAL, ACTIVE reservation."""
    from django.contrib.contenttypes.models import ContentType

    from koalixcrm.stock.models.stock_reservation import StockReservation

    document_type = None
    document_id = None
    if document is not None:
        document_type = ContentType.objects.get_for_model(document)
        document_id = document.pk

    reservation = StockReservation(
        workspace=workspace,
        variant=variant,
        location=location,
        batch=batch,
        serial_unit=serial_unit,
        kind=kind,
        document_type=document_type,
        document_id=document_id,
        qty_reserved=qty_reserved,
        uom=uom,
        rental_start=rental_start,
        rental_end=rental_end,
        expires_at=expires_at,
        status=ReservationLifecycleStatus.ACTIVE,
        reservation_status=ReservationConfirmationStatus.PROVISIONAL,
    )
    reservation.full_clean()
    reservation.save()
    return reservation


def _colliding_sent_reservation(reservation: "StockReservation"):
    from koalixcrm.stock.models.stock_reservation import StockReservation

    if reservation.serial_unit_id is None:
        return None
    qs = StockReservation.objects.filter(
        workspace=reservation.workspace,
        serial_unit_id=reservation.serial_unit_id,
        kind__in=(ReservationKind.RENTAL, ReservationKind.PROJECT_HOLD),
        status=ReservationLifecycleStatus.ACTIVE,
        sent_at__isnull=False,
    ).exclude(pk=reservation.pk)
    if reservation.rental_start is not None and reservation.rental_end is not None:
        qs = qs.filter(rental_start__lt=reservation.rental_end, rental_end__gt=reservation.rental_start)
    return qs.order_by("sent_at").first()


@transaction.atomic
def mark_sent(reservation: "StockReservation", *, occurred_at=None) -> "StockReservation":
    """SENT-equivalent: first-SENT-wins (ADR-0010 Amendment OQ-0012). The
    first competing reservation (same `serial_unit`, overlapping window)
    to call this wins; every later competitor is rejected with
    `ReservationConflict` (HTTP 409 at the view layer)."""
    collision = _colliding_sent_reservation(reservation)
    if collision is not None:
        raise ReservationConflict(
            _("Another reservation (#%(id)s) already holds this SerialUnit/window as SENT.")
            % {"id": collision.pk},
            colliding_reservation_id=collision.pk,
        )
    reservation.sent_at = occurred_at or timezone.now()
    reservation.full_clean()
    reservation.save()
    return reservation


def confirm(reservation: "StockReservation") -> "StockReservation":
    """ACCEPTED-equivalent: reservation becomes CONFIRMED and unchangeable
    until physical handover."""
    reservation.reservation_status = ReservationConfirmationStatus.CONFIRMED
    reservation.full_clean()
    reservation.save()
    return reservation


def cancel(reservation: "StockReservation", *, compensates_movement=None,
          occurred_at=None, uom=None, created_by=None) -> "StockReservation":
    """REJECTED/EXPIRED/CANCELLED-equivalent: release the reservation. If
    `compensates_movement` is given (the original soft-reservation
    `StockMovement`, e.g. the `rental_out`/`disposition=reserved` planning
    event), also posts a compensating `adjustment` movement referencing it
    (ADR-0010 Amendment OQ-0012)."""
    from koalixcrm.stock.services.movement_posting import post_movement

    with transaction.atomic():
        reservation.status = ReservationLifecycleStatus.CANCELLED
        reservation.full_clean()
        reservation.save()

        if compensates_movement is not None:
            post_movement(
                workspace=reservation.workspace,
                event_type=EventType.OBJECT_EVENT,
                business_step=BusinessStep.ADJUSTMENT,
                occurred_at=occurred_at or timezone.now(),
                variant=reservation.variant,
                qty=None,
                uom=uom or compensates_movement.uom,
                disposition=None,
                compensates=compensates_movement,
                created_by=created_by,
            )
    return reservation


def fulfill(reservation: "StockReservation") -> "StockReservation":
    """Physical handover: reservation transitions ACTIVE -> FULFILLED. Must
    be called before constructing the corresponding `RentalAssignment`
    (ADR-0013 Amendment OQ-0013)."""
    if reservation.status != ReservationLifecycleStatus.ACTIVE:
        raise ValidationError(_("Only an ACTIVE reservation can be fulfilled."))
    reservation.status = ReservationLifecycleStatus.FULFILLED
    reservation.full_clean()
    reservation.save()
    return reservation


def create_rental_soft_reservation(*, workspace, variant, serial_unit, uom,
                                   rental_start, rental_end, document=None,
                                   occurred_at=None, created_by=None):
    """Convenience wrapper for the ADR-0010 Amendment OQ-0010 rental-offer
    flow: creates the `StockReservation` (kind=RENTAL) and posts the
    soft-reservation `StockMovement` (`business_step=rental_out`,
    `qty=null`, `disposition=reserved`) in one transaction. Returns
    `(reservation, movement)`."""
    from koalixcrm.stock.services.movement_posting import post_movement

    with transaction.atomic():
        reservation = create_reservation(
            workspace=workspace,
            variant=variant,
            kind=ReservationKind.RENTAL,
            uom=uom,
            serial_unit=serial_unit,
            document=document,
            rental_start=rental_start,
            rental_end=rental_end,
        )
        movement = post_movement(
            workspace=workspace,
            event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RENTAL_OUT,
            occurred_at=occurred_at or timezone.now(),
            variant=variant,
            serial_unit=serial_unit,
            qty=None,
            uom=uom,
            disposition=Disposition.RESERVED,
            created_by=created_by,
        )
    return reservation, movement
