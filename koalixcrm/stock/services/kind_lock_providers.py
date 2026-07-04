# -*- coding: utf-8 -*-
"""Stage 4/6 lock-set membership providers (ADR-0019 kind-Unveränderlichkeit):
registers the existence of a `OnHandRecord`, `Batch`, `SerialUnit` or
`ProductionOrder` row for a `Product` (reached transitively via
`variant__product`/`product`) as a lock-set member via
`ProductKindPolicy.register_lock_provider`.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from koalixcrm.products.services.product_kind_policy import register_lock_provider

if TYPE_CHECKING:
    from koalixcrm.products.models.product import Product

_REGISTERED = False


def _has_stock_fact(product: "Product") -> bool:
    from koalixcrm.stock.models.batch import Batch
    from koalixcrm.stock.models.on_hand_record import OnHandRecord
    from koalixcrm.stock.models.serial_unit import SerialUnit

    return (
        OnHandRecord.objects.filter(variant__product=product).exists()
        or Batch.objects.filter(variant__product=product).exists()
        or SerialUnit.objects.filter(variant__product=product).exists()
    )


def _has_production_order(product: "Product") -> bool:
    from koalixcrm.stock.models.production_order import ProductionOrder

    return ProductionOrder.objects.filter(product=product).exists()


def register_stock_lock_providers() -> None:
    """Idempotent registration entry point, called from `StockConfig.ready()`."""
    global _REGISTERED
    if _REGISTERED:
        return
    register_lock_provider(_has_stock_fact)
    register_lock_provider(_has_production_order)
    _REGISTERED = True
