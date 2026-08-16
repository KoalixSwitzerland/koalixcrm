# -*- coding: utf-8 -*-
"""`OnHandRecord` — an atomic stock-quantity row keyed on `ProductVariant`
(ADR-0009; Amendment 2026-06-28 makes `ProductVariant` the sole,
authoritative stock key per ADR-0021 — there is no direct `Product` FK,
the product is reachable only via `variant.product`). REQ-0019 is the
requirement-level source for the field list and the composite uniqueness
constraint."""
from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.services.product_kind_policy import check_gate
from koalixcrm.stock.models.choices import OwnerType
from koalixcrm.stock.services.tracking_mode_policy import enforce_tracking_mode_coupling


class OnHandRecord(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    variant = models.ForeignKey("products.ProductVariant",
                                on_delete=models.PROTECT,
                                verbose_name=_("Product Variant"),
                                related_name="on_hand_records")
    location = models.ForeignKey("Location",
                                 on_delete=models.PROTECT,
                                 verbose_name=_("Location"),
                                 related_name="on_hand_records")
    batch = models.ForeignKey("Batch",
                              on_delete=models.PROTECT,
                              verbose_name=_("Batch"),
                              related_name="on_hand_records",
                              null=True,
                              blank=True)
    serial_unit = models.ForeignKey("SerialUnit",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Serial Unit"),
                                    related_name="on_hand_records",
                                    null=True,
                                    blank=True)
    handling_unit = models.ForeignKey("HandlingUnit",
                                      on_delete=models.SET_NULL,
                                      verbose_name=_("Handling Unit"),
                                      related_name="on_hand_records",
                                      null=True,
                                      blank=True)
    owner_type = models.CharField(verbose_name=_("Owner Type"),
                                  max_length=32,
                                  choices=OwnerType.choices,
                                  default=OwnerType.OWN)
    owner_party = models.ForeignKey("contacts.Party",
                                    on_delete=models.PROTECT,
                                    verbose_name=_("Owner Party"),
                                    related_name="owned_stock_records",
                                    null=True,
                                    blank=True)
    qty_on_hand = models.DecimalField(verbose_name=_("Quantity On Hand"),
                                      max_digits=18,
                                      decimal_places=4,
                                      default=Decimal("0"),
                                      validators=[MinValueValidator(Decimal("0"))])
    uom = models.ForeignKey("core.Unit",
                            on_delete=models.PROTECT,
                            verbose_name=_("Unit of Measure"))
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if self.variant_id is not None:
            check_gate("StockFact", self.variant.product.kind)
            enforce_tracking_mode_coupling(self.variant, self.batch, self.serial_unit)
        if (self.owner_type in (OwnerType.CUSTOMER_CONSIGNMENT, OwnerType.RENTAL, OwnerType.CUSTOMER_OWNED)
                and self.owner_party_id is None):
            raise ValidationError(
                _("owner_type=%(owner_type)s requires owner_party to be set.")
                % {"owner_type": self.owner_type}
            )
        if self.location_id is not None and not self.location.is_active:
            raise ValidationError(
                _("Cannot create an OnHandRecord at an inactive Location.")
            )
        if self.serial_unit_id is not None and self.qty_on_hand != Decimal("1"):
            raise ValidationError(
                _("A serial-tracked OnHandRecord must have qty_on_hand = 1.")
            )
        self._assert_no_exact_duplicate()

    def _assert_no_exact_duplicate(self) -> None:
        # UniqueConstraint below is the DB-level backstop, but SQL NULL
        # semantics treat two NULLs as distinct, so it does not by itself
        # reject two NONE-tracked rows that share every other key field
        # (REQ-0019 AC-2 requires exact-tuple rejection, NULLs included).
        duplicate_qs = OnHandRecord.objects.filter(
            workspace=self.workspace,
            variant=self.variant,
            location=self.location,
            batch=self.batch,
            serial_unit=self.serial_unit,
            owner_type=self.owner_type,
            owner_party=self.owner_party,
        )
        if self.pk is not None:
            duplicate_qs = duplicate_qs.exclude(pk=self.pk)
        if duplicate_qs.exists():
            raise ValidationError(
                _("A duplicate OnHandRecord already exists for this "
                  "(variant, location, batch, serial_unit, owner_type, owner_party) combination.")
            )

    def __str__(self) -> str:
        return f"{self.variant_id}@{self.location_id}: {self.qty_on_hand}"

    class Meta:
        app_label = "stock"
        db_table = "stock_onhandrecord"
        verbose_name = _("On-Hand Record")
        verbose_name_plural = _("On-Hand Records")
        ordering = ["variant", "location"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "variant", "location", "batch", "serial_unit", "owner_type", "owner_party"],
                name="uniq_onhandrecord_key",
            ),
        ]
        indexes = [
            models.Index(fields=["workspace", "variant", "location"], name="idx_onhandrecord_var_loc"),
        ]
