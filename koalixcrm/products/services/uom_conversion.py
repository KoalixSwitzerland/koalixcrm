# -*- coding: utf-8 -*-
"""Conversion-factor lookup for `UnitOfMeasureConversion` (ADR-0005, REQ-0013
AC-2): a stored `(product, A -> B, factor=f)` row also answers the reverse
`(product, B -> A)` query with `1/f`, without a second stored row."""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from koalixcrm.products.models.unit_of_measure_conversion import (
    UnitOfMeasureConversion,
)

if TYPE_CHECKING:
    from koalixcrm.core.models.unit import Unit
    from koalixcrm.products.models.product import Product


class NoConversionFound(Exception):
    def __init__(self, product: "Product", from_unit: "Unit", to_unit: "Unit") -> None:
        self.product = product
        self.from_unit = from_unit
        self.to_unit = to_unit

    def __str__(self) -> str:
        return (
            f"No UnitOfMeasureConversion for product {self.product!r} "
            f"between {self.from_unit} and {self.to_unit}"
        )


def get_conversion_factor(product: "Product", from_unit: "Unit", to_unit: "Unit") -> Decimal:
    """Return the conversion factor for `from_unit -> to_unit` on `product`.

    A direct stored row is used as-is; a stored reverse row
    `(to_unit -> from_unit, factor=f)` yields `1/f`. Raises
    `NoConversionFound` if neither direction is stored.
    """
    if from_unit == to_unit:
        return Decimal(1)

    direct = UnitOfMeasureConversion.objects.filter(
        product=product, from_unit=from_unit, to_unit=to_unit
    ).first()
    if direct is not None:
        return direct.factor

    reverse = UnitOfMeasureConversion.objects.filter(
        product=product, from_unit=to_unit, to_unit=from_unit
    ).first()
    if reverse is not None:
        return Decimal(1) / reverse.factor

    raise NoConversionFound(product, from_unit, to_unit)
