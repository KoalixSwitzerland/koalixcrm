# -*- coding: utf-8 -*-
"""`ProductMedia` — S3/MinIO-backed media references (ADR-0003).

`media_type` knows exactly `image`, `datasheet` and `certificate`; any
other value is rejected. Per ADR-0021's keying table, media exists at
*both* the `Product` and `ProductVariant` level — the effective media pool
of a variant is the union of product-level and variant-level media — so
exactly one of `product` / `variant` is set on a given row (enforced in
`clean()`).
"""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.models.choices import ProductMediaType


class ProductMedia(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey("Product",
                                on_delete=models.CASCADE,
                                verbose_name=_("Product"),
                                related_name="media_items",
                                null=True,
                                blank=True)
    variant = models.ForeignKey("ProductVariant",
                                on_delete=models.CASCADE,
                                verbose_name=_("Product Variant"),
                                related_name="media_items",
                                null=True,
                                blank=True)
    media_type = models.CharField(verbose_name=_("Media Type"),
                                  max_length=32,
                                  choices=ProductMediaType.choices)
    object_key = models.CharField(verbose_name=_("Object Storage Key"), max_length=1024)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    def clean(self) -> None:
        super().clean()
        if bool(self.product_id) == bool(self.variant_id):
            raise ValidationError(
                _("ProductMedia must reference exactly one of Product or ProductVariant.")
            )

    def __str__(self) -> str:
        return f"{self.get_media_type_display()}: {self.object_key}"

    class Meta:
        app_label = "products"
        db_table = "products_productmedia"
        verbose_name = _("Product Media")
        verbose_name_plural = _("Product Media")
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(product__isnull=False, variant__isnull=True)
                    | models.Q(product__isnull=True, variant__isnull=False)
                ),
                name="product_media_exactly_one_of_product_or_variant",
            )
        ]
