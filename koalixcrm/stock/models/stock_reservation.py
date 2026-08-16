# -*- coding: utf-8 -*-
"""`StockReservation` — the sole authoritative source of occupancy for the
availability calendar (ADR-0010, incl. Amendments OQ-0011/OQ-0012/OQ-0013;
Amendment 2026-07-04 rekeys the FK from `Product` to `ProductVariant` per
ADR-0021). Carries a generic document reference (offer/order) instead of a
direct FK, keeping the stock app importable without a `contracts`
dependency."""
from __future__ import annotations

from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.stock.models.choices import (
    ReservationConfirmationStatus,
    ReservationKind,
    ReservationLifecycleStatus,
    ReservationType,
)


class StockReservation(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    variant = models.ForeignKey("products.ProductVariant",
                                on_delete=models.PROTECT,
                                verbose_name=_("Product Variant"),
                                related_name="stock_reservations")
    location = models.ForeignKey("Location",
                                 on_delete=models.PROTECT,
                                 verbose_name=_("Location"),
                                 related_name="stock_reservations",
                                 null=True,
                                 blank=True,
                                 help_text=_("Null = any location of this tenant."))
    batch = models.ForeignKey("Batch",
                              on_delete=models.PROTECT,
                              verbose_name=_("Batch"),
                              related_name="stock_reservations",
                              null=True,
                              blank=True)
    serial_unit = models.ForeignKey("SerialUnit",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Serial Unit"),
                                    related_name="stock_reservations",
                                    null=True,
                                    blank=True,
                                    help_text=_("Set for kind = RENTAL and kind = PROJECT_HOLD."))
    kind = models.CharField(verbose_name=_("Kind"), max_length=16, choices=ReservationKind.choices)
    reservation_type = models.CharField(verbose_name=_("Reservation Type"),
                                        max_length=32,
                                        choices=ReservationType.choices,
                                        default=ReservationType.BOOKED)
    reservation_status = models.CharField(verbose_name=_("Reservation Status"),
                                          max_length=16,
                                          choices=ReservationConfirmationStatus.choices,
                                          default=ReservationConfirmationStatus.PROVISIONAL)
    document_type = models.ForeignKey("contenttypes.ContentType",
                                      on_delete=models.PROTECT,
                                      verbose_name=_("Document Type"),
                                      null=True,
                                      blank=True)
    document_id = models.PositiveIntegerField(verbose_name=_("Document ID"), null=True, blank=True)
    document = GenericForeignKey("document_type", "document_id")
    qty_reserved = models.DecimalField(verbose_name=_("Quantity Reserved"),
                                       max_digits=18,
                                       decimal_places=4,
                                       null=True,
                                       blank=True,
                                       help_text=_("Nullable for serial-number-bound reservations."))
    uom = models.ForeignKey("core.Unit",
                            on_delete=models.PROTECT,
                            verbose_name=_("Unit of Measure"),
                            null=True,
                            blank=True)
    rental_start = models.DateTimeField(verbose_name=_("Rental Start"), null=True, blank=True)
    rental_end = models.DateTimeField(verbose_name=_("Rental End"), null=True, blank=True)
    expires_at = models.DateTimeField(verbose_name=_("Expires At"), null=True, blank=True)
    sent_at = models.DateTimeField(
        verbose_name=_("Sent At"),
        null=True,
        blank=True,
        help_text=_("ADR-0010 Amendment OQ-0012 first-SENT-wins concurrency marker: the "
                    "timestamp this reservation's document-side transition to SENT was "
                    "recorded, via services/reservation_lifecycle.py:mark_sent(). Null = not "
                    "yet SENT. Since the offer/order document itself lives outside the stock "
                    "app (ADR-0010 generic document reference), this field is the "
                    "service-level FIFO race marker; see Stage 5 deferral notes."),
    )
    status = models.CharField(verbose_name=_("Status"),
                              max_length=16,
                              choices=ReservationLifecycleStatus.choices,
                              default=ReservationLifecycleStatus.ACTIVE)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if self.kind in (ReservationKind.RENTAL, ReservationKind.PROJECT_HOLD) and self.serial_unit_id is None:
            raise ValidationError(
                _("kind=%(kind)s requires a serial_unit to be set.") % {"kind": self.kind}
            )
        if self.serial_unit_id is not None and self.variant_id is not None:
            if self.serial_unit.variant_id != self.variant_id:
                raise ValidationError(
                    _("StockReservation.serial_unit must belong to the same ProductVariant.")
                )
        if self.kind == ReservationKind.RENTAL:
            if self.rental_start is not None and self.rental_end is not None:
                if self.rental_start >= self.rental_end:
                    raise ValidationError(
                        _("rental_start must be strictly before rental_end.")
                    )
        if self.qty_reserved is not None and self.qty_reserved <= Decimal("0"):
            raise ValidationError(
                _("qty_reserved must be strictly positive when set.")
            )

    def __str__(self) -> str:
        return f"{self.kind}#{self.pk} {self.variant_id} ({self.status}/{self.reservation_status})"

    class Meta:
        app_label = "stock"
        db_table = "stock_stockreservation"
        verbose_name = _("Stock Reservation")
        verbose_name_plural = _("Stock Reservations")
        ordering = ["-date_of_creation"]
        indexes = [
            models.Index(fields=["workspace", "variant", "location"], name="idx_stockreservation_var_loc"),
            models.Index(fields=["workspace", "serial_unit", "status"], name="idx_stockreservation_serial_st"),
            models.Index(fields=["workspace", "kind", "status"], name="idx_stockreservation_kind_st"),
        ]
