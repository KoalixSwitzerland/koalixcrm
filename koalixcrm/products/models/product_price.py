# -*- coding: utf-8 -*-
"""`ProductPrice` — ADR-0021 Amendment 2026-06-28 (ADR-0005 Amendment): keyed
to `ProductVariant` (the sellable SKU), not `Product` — price is variant-
specific (e.g. different pack sizes of the same `Product` carry their own
`ProductPrice` rows). `price_list` (ADR-0005/REQ-0012) groups prices by
channel or customer segment; a `ProductPrice` without a `price_list` FK is
the workspace-wide default price (three-level price precedence)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.products.models.price import Price


class ProductPrice(Price):
    # 3-phase FK lift (product_type -> variant) complete as of migration
    # 0013: phase 1 (0011) added `variant` nullable alongside the legacy
    # `product_type` FK; phase 2 (0012) backfilled `variant`; phase 3 (0013,
    # this state) drops `product_type` and makes `variant` non-nullable.
    variant = models.ForeignKey("ProductVariant",
                                on_delete=models.CASCADE,
                                verbose_name=_("Product Variant"),
                                related_name="prices")
    price_list = models.ForeignKey("PriceList",
                                   on_delete=models.PROTECT,
                                   verbose_name=_("Price List"),
                                   related_name="prices",
                                   null=True,
                                   blank=True)

    def __str__(self) -> str:
        return str(self.price) + " " + str(self.currency.short_name)

    class Meta:
        app_label = "products"
        db_table = "crm_productprice"
        verbose_name = _('Product Price')
        verbose_name_plural = _('Product Prices')
