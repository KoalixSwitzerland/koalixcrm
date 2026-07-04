# -*- coding: utf-8 -*-
"""`ProductAttributeValueBase` — shared abstract base for the six typed EAV
value tables (ADR-0004): `ProductAttributeString`, `ProductAttributeInt`,
`ProductAttributeDecimal`, `ProductAttributeBool`, `ProductAttributeEnum`,
`ProductAttributeReference`.

Deliberately *not* a single polymorphic value table (ADR-0004 rejects that
design: cast expressions on a generic `value` column defeat B-Tree
indexing at 10k+ SKUs). Each concrete subclass adds exactly one typed
`value` column.

Carries the ADR-0021 Option A variant keying: a nullable `variant` FK. A
row with `variant IS NULL` is the product value; a row with `variant` set
is the variant-level override for that variant. The composite index/
uniqueness is on `(product, variant, attribute_definition)` per ADR-0004
Amendment 2026-06-28.

`imported_at` / `source_mapping` support the ADR-0018 source-priority rule:
`imported_at IS NULL` marks an operator-set explicit value (highest
priority); a non-null `imported_at` marks a Layer-3-adapter-imported value,
timestamped so a later import can supersede an earlier one. Because the
row is unique per (product, variant, attribute_definition), "last imported
wins" is enforced structurally by upsert — see
`koalixcrm.products.services.canonical_attributes.import_canonical_value`,
which additionally refuses to overwrite an explicit operator value with an
import (ADR-0018 §Quellpriorität)."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class ProductAttributeValueBase(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="%(class)s_values",
    )
    variant = models.ForeignKey(
        "ProductVariant",
        on_delete=models.CASCADE,
        verbose_name=_("Variant"),
        related_name="%(class)s_values",
        null=True,
        blank=True,
    )
    attribute_definition = models.ForeignKey(
        "AttributeDefinition",
        on_delete=models.CASCADE,
        verbose_name=_("Attribute Definition"),
        related_name="%(class)s_values",
    )
    source_mapping = models.ForeignKey(
        "ProductAttributeMapping",
        on_delete=models.SET_NULL,
        verbose_name=_("Source Mapping"),
        related_name="+",
        null=True,
        blank=True,
    )
    imported_at = models.DateTimeField(verbose_name=_("Imported At"), null=True, blank=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    class Meta:
        abstract = True
