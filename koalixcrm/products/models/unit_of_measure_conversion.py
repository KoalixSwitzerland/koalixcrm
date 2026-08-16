# -*- coding: utf-8 -*-
"""`UnitOfMeasureConversion` — product-specific unit conversions (ADR-0005,
REQ-0013). FK on `Product` (not `ProductVariant`): conversions such as
'piece <-> box of 12' are usually defined product-wide per ADR-0005's
2026-06-28 amendment. A variant needing its own rate gets its own row with
a FK to that `ProductVariant` instead (not modelled yet in this stage —
the ADR states this extension needs no further ADR when it happens)."""
from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class UnitOfMeasureConversion(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey("Product",
                                on_delete=models.CASCADE,
                                verbose_name=_("Product"),
                                related_name="uom_conversions")
    from_unit = models.ForeignKey("core.Unit",
                                  on_delete=models.CASCADE,
                                  verbose_name=_("From Unit"),
                                  related_name="+")
    to_unit = models.ForeignKey("core.Unit",
                                on_delete=models.CASCADE,
                                verbose_name=_("To Unit"),
                                related_name="+")
    factor = models.DecimalField(verbose_name=_("Conversion Factor"),
                                 max_digits=20,
                                 decimal_places=10,
                                 validators=[MinValueValidator(Decimal("0.0000000001"))])
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product_id}: {self.from_unit.short_name} -> {self.to_unit.short_name} ({self.factor})"

    class Meta:
        app_label = "products"
        db_table = "products_unitofmeasureconversion"
        verbose_name = _("Unit of Measure Conversion")
        verbose_name_plural = _("Unit of Measure Conversions")
        ordering = ["product_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "from_unit", "to_unit"],
                name="uom_conversion_unique_product_from_to",
            ),
        ]
