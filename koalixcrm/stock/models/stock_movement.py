# -*- coding: utf-8 -*-
"""`StockMovement` — the immutable EPCIS-2.0-oriented stock movement and
lifecycle event log (ADR-0011). Rows are append-only: `save()` refuses any
attempt to modify an already-persisted row, and `delete()` is refused by
default (ADR-0011 retention floor, `services/movement_retention.py`).

`variant` is a mandatory FK (Amendment 2026-07-04, OQ-0019) even though
`product` remains its own field per the ADR-0011 entity table (both are
kept; `product` is normally `variant.product`, carried explicitly so the
log is queryable without a join in the common case).

Only the posting service (`services/movement_posting.py`) is an authorized
write path that also updates `OnHandRecord`/`StockBalance` synchronously;
direct `StockMovement.objects.create(...)` calls bypass that and must not
be used outside the service."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.stock.models.choices import BusinessStep, Disposition, EventType, OwnerType
from koalixcrm.stock.services.movement_retention import assert_deletable


class StockMovement(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    event_type = models.CharField(verbose_name=_("Event Type"),
                                  max_length=32,
                                  choices=EventType.choices)
    business_step = models.CharField(verbose_name=_("Business Step"),
                                     max_length=32,
                                     choices=BusinessStep.choices)
    occurred_at = models.DateTimeField(verbose_name=_("Occurred At"))
    recorded_at = models.DateTimeField(verbose_name=_("Recorded At"), auto_now_add=True)
    source_location = models.ForeignKey("Location",
                                        on_delete=models.PROTECT,
                                        verbose_name=_("Source Location"),
                                        related_name="movements_from",
                                        null=True,
                                        blank=True)
    destination_location = models.ForeignKey("Location",
                                             on_delete=models.PROTECT,
                                             verbose_name=_("Destination Location"),
                                             related_name="movements_to",
                                             null=True,
                                             blank=True)
    product = models.ForeignKey("products.Product",
                                on_delete=models.PROTECT,
                                verbose_name=_("Product"),
                                related_name="stock_movements")
    variant = models.ForeignKey("products.ProductVariant",
                                on_delete=models.PROTECT,
                                verbose_name=_("Product Variant"),
                                related_name="stock_movements")
    batch = models.ForeignKey("Batch",
                              on_delete=models.PROTECT,
                              verbose_name=_("Batch"),
                              related_name="movements",
                              null=True,
                              blank=True)
    serial_unit = models.ForeignKey("SerialUnit",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Serial Unit"),
                                    related_name="movements",
                                    null=True,
                                    blank=True)
    handling_unit = models.ForeignKey("HandlingUnit",
                                      on_delete=models.SET_NULL,
                                      verbose_name=_("Handling Unit"),
                                      related_name="movements",
                                      null=True,
                                      blank=True)
    parent_serial_unit = models.ForeignKey("SerialUnit",
                                           on_delete=models.PROTECT,
                                           verbose_name=_("Parent Serial Unit"),
                                           related_name="child_movements",
                                           null=True,
                                           blank=True,
                                           help_text=_("AGGREGATION_EVENT parent unit when the "
                                                       "finished good's tracking_mode = SERIAL."))
    parent_batch = models.ForeignKey("Batch",
                                     on_delete=models.PROTECT,
                                     verbose_name=_("Parent Batch"),
                                     related_name="child_movements",
                                     null=True,
                                     blank=True,
                                     help_text=_("AGGREGATION_EVENT parent batch when the "
                                                 "finished good's tracking_mode = BATCH."))
    aggregation_group = models.UUIDField(verbose_name=_("Aggregation Group"), null=True, blank=True)
    qty = models.DecimalField(verbose_name=_("Quantity"),
                              max_digits=18,
                              decimal_places=4,
                              null=True,
                              blank=True,
                              help_text=_("Null = quantity-less lifecycle event."))
    uom = models.ForeignKey("core.Unit",
                            on_delete=models.PROTECT,
                            verbose_name=_("Unit of Measure"),
                            null=True,
                            blank=True)
    reason_code = models.ForeignKey("MovementReasonCode",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Reason Code"),
                                    related_name="movements",
                                    null=True,
                                    blank=True)
    document_type = models.ForeignKey("contenttypes.ContentType",
                                      on_delete=models.PROTECT,
                                      verbose_name=_("Document Type"),
                                      null=True,
                                      blank=True)
    document_id = models.PositiveIntegerField(verbose_name=_("Document ID"), null=True, blank=True)
    owner_type = models.CharField(verbose_name=_("Owner Type"),
                                  max_length=32,
                                  choices=OwnerType.choices,
                                  default=OwnerType.OWN)
    owner_party = models.ForeignKey("contacts.Party",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Owner Party"),
                                    related_name="stock_movements",
                                    null=True,
                                    blank=True)
    disposition = models.CharField(verbose_name=_("Disposition"),
                                   max_length=32,
                                   choices=Disposition.choices,
                                   null=True,
                                   blank=True)
    idempotency_key = models.UUIDField(verbose_name=_("Idempotency Key"))
    compensates = models.ForeignKey("self",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Compensates"),
                                    related_name="compensating_movements",
                                    null=True,
                                    blank=True)
    created_by = models.ForeignKey("auth.User",
                                   on_delete=models.SET_NULL,
                                   verbose_name=_("Created By"),
                                   related_name="stock_movements",
                                   null=True,
                                   blank=True)

    def clean(self) -> None:
        super().clean()
        if self.event_type == EventType.AGGREGATION_EVENT and not self.aggregation_group:
            raise ValidationError(
                _("aggregation_group is mandatory for event_type = AGGREGATION_EVENT.")
            )
        if self.business_step == BusinessStep.INVENTORYING and self.qty is not None:
            raise ValidationError(
                _("business_step = inventorying must carry qty = null (verification-only event).")
            )

    def save(self, *args, **kwargs):
        if self.pk is not None and not self._state.adding:
            raise ValidationError(
                _("StockMovement rows are immutable; updates are refused. "
                  "Corrections must be posted as a new, compensating StockMovement.")
            )
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        assert_deletable(self)
        return super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.business_step}@{self.occurred_at}: {self.variant_id}"

    class Meta:
        app_label = "stock"
        db_table = "stock_stockmovement"
        verbose_name = _("Stock Movement")
        verbose_name_plural = _("Stock Movements")
        ordering = ["-occurred_at", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "idempotency_key"],
                name="uniq_stockmovement_idempotency_key",
            ),
        ]
        indexes = [
            models.Index(fields=["workspace", "variant", "occurred_at"], name="idx_stockmovement_var_time"),
            models.Index(fields=["workspace", "business_step"], name="idx_stockmovement_bizstep"),
            models.Index(fields=["aggregation_group"], name="idx_stockmovement_agggroup"),
        ]
