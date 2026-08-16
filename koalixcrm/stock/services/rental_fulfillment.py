# -*- coding: utf-8 -*-
"""ADR-0013 (Amendment 2026-05-04, OQ-0013): physical rental handover and
return. `RentalAssignment` is only ever created for a `StockReservation`
that is already `FULFILLED` — this module performs both the reservation
transition (`services/reservation_lifecycle.fulfill`) and the
`StockMovement` posting (`disposition=in_possession` / `returned`) in the
same transaction as the `RentalAssignment` row.

Justification: transactional integrity — combines reservation_lifecycle.fulfill, movement_posting.post_movement and RentalAssignment creation in one DB transaction; still needed with the microservice fleet deleted. (Tier-2 GRANTED by architect.)"""
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
    OwnerType,
    ReservationKind,
    RentalAssignmentStatus,
)
from koalixcrm.stock.services.movement_posting import post_movement
from koalixcrm.stock.services.reservation_lifecycle import fulfill

if TYPE_CHECKING:
    from koalixcrm.stock.models.rental_assignment import RentalAssignment
    from koalixcrm.stock.models.stock_reservation import StockReservation


def hand_over(*, reservation: "StockReservation", party, source_location=None,
             destination_location=None, return_due_date=None, occurred_at=None,
             document=None, created_by=None) -> "RentalAssignment":
    """Physical handover: transitions `reservation` (kind=RENTAL,
    status=ACTIVE) to FULFILLED, posts the `rental_out`/`in_possession`
    `StockMovement`, and creates the `RentalAssignment`."""
    from django.contrib.contenttypes.models import ContentType

    from koalixcrm.stock.models.rental_assignment import RentalAssignment

    if reservation.kind != ReservationKind.RENTAL:
        raise ValidationError(_("hand_over() requires a kind=RENTAL reservation."))

    occurred_at = occurred_at or timezone.now()

    with transaction.atomic():
        fulfill(reservation)

        post_movement(
            workspace=reservation.workspace,
            event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RENTAL_OUT,
            occurred_at=occurred_at,
            variant=reservation.variant,
            serial_unit=reservation.serial_unit,
            source_location=source_location,
            destination_location=destination_location,
            qty=None,
            disposition=Disposition.IN_POSSESSION,
            owner_type=OwnerType.RENTAL,
            owner_party=party,
            created_by=created_by,
        )

        document_type = None
        document_id = None
        if document is not None:
            document_type = ContentType.objects.get_for_model(document)
            document_id = document.pk

        assignment = RentalAssignment(
            workspace=reservation.workspace,
            serial_unit=reservation.serial_unit,
            reservation=reservation,
            party=party,
            document_type=document_type,
            document_id=document_id,
            rental_start=occurred_at,
            return_due_date=return_due_date,
            status=RentalAssignmentStatus.ACTIVE,
        )
        assignment.full_clean()
        assignment.save()

    return assignment


def return_unit(*, assignment: "RentalAssignment", condition_at_return=None,
                source_location=None, destination_location=None,
                occurred_at=None, created_by=None) -> "RentalAssignment":
    """Physical return: posts the `rental_return`/`returned` `StockMovement`
    and closes out the `RentalAssignment`."""
    occurred_at = occurred_at or timezone.now()

    with transaction.atomic():
        post_movement(
            workspace=assignment.workspace,
            event_type=EventType.OBJECT_EVENT,
            business_step=BusinessStep.RENTAL_RETURN,
            occurred_at=occurred_at,
            variant=assignment.reservation.variant,
            serial_unit=assignment.serial_unit,
            source_location=source_location,
            destination_location=destination_location,
            qty=None,
            disposition=Disposition.RETURNED,
            owner_type=OwnerType.OWN,
            owner_party=assignment.party,
            created_by=created_by,
        )
        assignment.returned_at = occurred_at
        assignment.status = RentalAssignmentStatus.RETURNED
        if condition_at_return is not None:
            assignment.condition_at_return = condition_at_return
        assignment.full_clean()
        assignment.save()

    return assignment
