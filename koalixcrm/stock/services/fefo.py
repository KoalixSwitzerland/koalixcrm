# -*- coding: utf-8 -*-
"""ADR-0012 FEFO/FIFO pick-order helpers.

FEFO: 1. non-quarantined batches, 2. ascending `expiry_date` (nulls last),
3. tie-break ascending `production_date`.
FIFO fallback (no expiry dates): ascending `received_at`.

Justification: framework — pure QuerySet ordering helper (order_by/F()) consumed inline by pick-list construction within the same app; still needed with the microservice fleet deleted.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import F, QuerySet

if TYPE_CHECKING:
    from koalixcrm.products.models.product_variant import ProductVariant
    from koalixcrm.stock.models.batch import Batch


def fefo_order_batches(variant: "ProductVariant", include_quarantined: bool = False) -> "QuerySet[Batch]":
    from koalixcrm.stock.models.batch import Batch

    qs = Batch.objects.filter(workspace=variant.workspace, variant=variant)
    if not include_quarantined:
        qs = qs.filter(quarantine=False)
    return qs.order_by(F("expiry_date").asc(nulls_last=True), "production_date")


def fifo_order_batches(variant: "ProductVariant", include_quarantined: bool = False) -> "QuerySet[Batch]":
    from koalixcrm.stock.models.batch import Batch

    qs = Batch.objects.filter(workspace=variant.workspace, variant=variant)
    if not include_quarantined:
        qs = qs.filter(quarantine=False)
    return qs.order_by("received_at")
