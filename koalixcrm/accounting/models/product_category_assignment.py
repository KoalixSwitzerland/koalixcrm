# -*- coding: utf-8 -*-
"""Optional-peer linkage between `products.ProductType` and
`accounting.ProductCategory`.

Historically `products.ProductType` carried a FK `accounting_product_category`
pointing at `accounting.ProductCategory`. That coupling broke the
fork-isolation invariant: WFS does not install `koalixcrm.accounting`.
CR-2c relocates the linkage here as a one-to-one assignment.
"""

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.accounting.models.product_category import ProductCategory


class ProductCategoryAssignment(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_type = models.OneToOneField(
        "products.ProductType",
        on_delete=models.CASCADE,
        related_name="product_category_assignment",
        verbose_name=_("Product Type"),
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        verbose_name=_("Accounting Product Category"),
        related_name="product_type_assignments",
    )

    class Meta:
        app_label = "accounting"
        verbose_name = _("Product Category Assignment")
        verbose_name_plural = _("Product Category Assignments")

    def __str__(self) -> str:
        return _("Category for product: ") + str(self.product_type)
