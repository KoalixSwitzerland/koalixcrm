# -*- coding: utf-8 -*-
"""Stage 3 lock-set membership providers (ADR-0019 kind-Unveränderlichkeit):
registers `BillOfMaterials` and `ServiceProfile` existence as lock-set
members via `ProductKindPolicy.register_lock_provider`. `ProductionOrder`
and the stock-fact lock-set members (`StockMovement`/`SerialUnit`/`Batch`/
`OnHandRecord`) are later stages' responsibility."""
from __future__ import annotations

from typing import TYPE_CHECKING

from koalixcrm.products.services.product_kind_policy import register_lock_provider

if TYPE_CHECKING:
    from koalixcrm.products.models.product import Product

_REGISTERED = False


def _has_bill_of_materials(product: "Product") -> bool:
    from koalixcrm.products.models.bill_of_materials import BillOfMaterials

    return BillOfMaterials.objects.filter(product=product).exists()


def _has_service_profile(product: "Product") -> bool:
    from koalixcrm.products.models.service_profile import ServiceProfile

    return ServiceProfile.objects.filter(product=product).exists()


def register_stage3_lock_providers() -> None:
    """Idempotent registration entry point, called from `ProductsConfig.ready()`."""
    global _REGISTERED
    if _REGISTERED:
        return
    register_lock_provider(_has_bill_of_materials)
    register_lock_provider(_has_service_profile)
    _REGISTERED = True
