# -*- coding: utf-8 -*-
"""Phase 2 of the `ProductPrice.product_type` -> `ProductPrice.variant` FK
lift (ADR-0021 Amendment 2026-06-28 / ADR-0005 Amendment): backfills
`variant` for every existing `ProductPrice` row.

For each row, reuses the referenced `Product`'s lowest-pk `ProductVariant`
if one exists, else creates a default variant (ADR-0021: "jedes `Product`
besitzt >= 1 `ProductVariant`" — legacy data predating that invariant is
backfilled here rather than left inconsistent)."""
from __future__ import annotations

from django.db import migrations


def backfill_variant(apps, schema_editor):
    ProductVariant = apps.get_model("products", "ProductVariant")
    ProductPrice = apps.get_model("products", "ProductPrice")

    for price in ProductPrice.objects.filter(variant__isnull=True).iterator():
        product_id = price.product_type_id
        if product_id is None:
            continue
        variant = ProductVariant.objects.filter(product_id=product_id).order_by("id").first()
        if variant is None:
            Product = apps.get_model("products", "Product")
            product = Product.objects.get(pk=product_id)
            sku_seed = product.product_type_identifier or f"PRODUCT-{product.id}"
            variant = ProductVariant.objects.create(
                workspace_id=product.workspace_id,
                product_id=product.id,
                sku=f"{sku_seed}-DEFAULT",
            )
        price.variant_id = variant.id
        price.save(update_fields=["variant_id"])


def noop_reverse(apps, schema_editor):
    """No reverse data movement: `product_type` is still populated at this
    migration state, so reversing is a no-op (the forward operation is
    additive/backfill-only, not destructive)."""


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0011_stage3_pricing_sourcing_service_passport"),
    ]

    operations = [
        migrations.RunPython(backfill_variant, noop_reverse),
    ]
