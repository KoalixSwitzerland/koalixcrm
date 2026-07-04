# -*- coding: utf-8 -*-
"""`ProductSupply` — links a `Product` to a supplier `Party` (ADR-0006,
REQ-0014). Kind-agnostic (ADR-0019 Gating-Matrix): allowed for every `kind`,
including `SERVICE` (a subcontractor link)."""
from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.services.product_supply_validation import (
    validate_supplier_role,
)


class ProductSupply(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey("Product",
                                on_delete=models.CASCADE,
                                verbose_name=_("Product"),
                                related_name="supplies")
    supplier = models.ForeignKey("contacts.Party",
                                 on_delete=models.PROTECT,
                                 verbose_name=_("Supplier"),
                                 related_name="product_supplies")
    supplier_sku = models.CharField(verbose_name=_("Supplier SKU"),
                                    max_length=200,
                                    null=True,
                                    blank=True)
    lead_time_days = models.PositiveIntegerField(verbose_name=_("Lead Time (working days)"),
                                                 null=True,
                                                 blank=True)
    moq = models.DecimalField(verbose_name=_("Minimum Order Quantity"),
                              max_digits=17,
                              decimal_places=4,
                              null=True,
                              blank=True,
                              validators=[MinValueValidator(Decimal("0.0001"))])
    purchase_price = models.DecimalField(verbose_name=_("Purchase Price"),
                                         max_digits=17,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    purchase_currency = models.ForeignKey("core.Currency",
                                          on_delete=models.PROTECT,
                                          verbose_name=_("Purchase Currency"),
                                          related_name="+",
                                          null=True,
                                          blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if self.supplier_id is not None:
            validate_supplier_role(self.supplier)

    def __str__(self) -> str:
        return f"{self.product_id} <- {self.supplier}"

    class Meta:
        app_label = "products"
        db_table = "products_productsupply"
        verbose_name = _("Product Supply")
        verbose_name_plural = _("Product Supplies")
        ordering = ["product_id"]
        constraints = [
            models.UniqueConstraint(fields=["product", "supplier"], name="productsupply_unique_product_supplier"),
        ]
