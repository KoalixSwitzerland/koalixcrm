# -*- coding: utf-8 -*-
"""`RentalAssignment` — the mietvertragsspezifische specialization of
`StockReservation` (ADR-0013, Amendment 2026-05-04 OQ-0013). Created at
physical handover; `reservation` is a mandatory FK to the `StockReservation`
it fulfills (`kind = RENTAL`, `status = FULFILLED` by the time the
assignment is created — the posting service sets that transition before
constructing this row)."""
from __future__ import annotations

from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.stock.models.choices import (
    RentalAssignmentStatus,
    ReservationKind,
    ReservationLifecycleStatus,
    SerialConditionState,
)


class RentalAssignment(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    serial_unit = models.ForeignKey("SerialUnit",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Serial Unit"),
                                    related_name="rental_assignments",
                                    null=True,
                                    blank=True)
    on_hand_record = models.ForeignKey("OnHandRecord",
                                       on_delete=models.PROTECT,
                                       verbose_name=_("On-Hand Record"),
                                       related_name="rental_assignments",
                                       null=True,
                                       blank=True)
    reservation = models.ForeignKey("StockReservation",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Fulfilled Reservation"),
                                    related_name="rental_assignments")
    party = models.ForeignKey("contacts.Party",
                              on_delete=models.PROTECT,
                              verbose_name=_("Renter"),
                              related_name="rental_assignments")
    document_type = models.ForeignKey("contenttypes.ContentType",
                                      on_delete=models.PROTECT,
                                      verbose_name=_("Document Type"),
                                      null=True,
                                      blank=True)
    document_id = models.PositiveIntegerField(verbose_name=_("Document ID"), null=True, blank=True)
    document = GenericForeignKey("document_type", "document_id")
    rental_start = models.DateTimeField(verbose_name=_("Rental Start (physical handover)"))
    return_due_date = models.DateField(verbose_name=_("Return Due Date"), null=True, blank=True)
    returned_at = models.DateTimeField(verbose_name=_("Returned At"), null=True, blank=True)
    status = models.CharField(verbose_name=_("Status"),
                              max_length=16,
                              choices=RentalAssignmentStatus.choices,
                              default=RentalAssignmentStatus.ACTIVE)
    condition_at_return = models.CharField(verbose_name=_("Condition At Return"),
                                           max_length=16,
                                           choices=SerialConditionState.choices,
                                           null=True,
                                           blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if self.reservation_id is not None:
            if self.reservation.kind != ReservationKind.RENTAL:
                raise ValidationError(
                    _("RentalAssignment.reservation must have kind = RENTAL.")
                )
            if self.reservation.status != ReservationLifecycleStatus.FULFILLED:
                raise ValidationError(
                    _("RentalAssignment.reservation must be FULFILLED before the assignment "
                      "is created.")
                )
            if (self.serial_unit_id is not None
                    and self.reservation.serial_unit_id is not None
                    and self.serial_unit_id != self.reservation.serial_unit_id):
                raise ValidationError(
                    _("RentalAssignment.serial_unit must match the fulfilled reservation's "
                      "serial_unit.")
                )

    def __str__(self) -> str:
        return f"RentalAssignment#{self.pk} {self.serial_unit_id} -> {self.party_id}"

    class Meta:
        app_label = "stock"
        db_table = "stock_rentalassignment"
        verbose_name = _("Rental Assignment")
        verbose_name_plural = _("Rental Assignments")
        ordering = ["-rental_start"]
        indexes = [
            models.Index(fields=["workspace", "serial_unit", "status"], name="idx_rentalassign_serial_status"),
            models.Index(fields=["workspace", "return_due_date"], name="idx_rentalassign_due"),
        ]
