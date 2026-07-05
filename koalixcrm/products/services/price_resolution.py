# -*- coding: utf-8 -*-
"""Three-level price precedence (ADR-0005 §Drei-Ebenen-Preisvorrang,
REQ-0012 AC-2), resolved against `ProductVariant` (ADR-0021 Amendment):

1. `ProductPrice` with an explicit `PriceList` FK matching the request.
2. `ProductPrice` without a `PriceList` FK (workspace-wide default).
3. `customer_group_transform` factor applied to the price found in 1 or 2.

Pure function, no side effects; identical inputs always yield the same
result (ADR-0005 determinism requirement).

Justification: framework — deterministic ORM read over ProductPrice, resolved inline wherever a price must be frozen onto a document line; still needed with the microservice fleet deleted."""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from koalixcrm.products.models.product_price import ProductPrice

if TYPE_CHECKING:
    from koalixcrm.contacts.models.party import Party
    from koalixcrm.core.models.currency import Currency
    from koalixcrm.core.models.unit import Unit
    from koalixcrm.products.models.price_list import PriceList
    from koalixcrm.products.models.product_variant import ProductVariant


class NoPriceFound(Exception):
    def __init__(
        self,
        variant: "ProductVariant",
        date: datetime.date,
        party: "Party | None",
        currency: "Currency",
        price_list: "PriceList | None",
    ) -> None:
        self.variant = variant
        self.date = date
        self.party = party
        self.currency = currency
        self.price_list = price_list

    def __str__(self) -> str:
        return (
            f"No price for variant {self.variant!r} on {self.date} in currency "
            f"{self.currency!r} (price_list={self.price_list!r})"
        )


def _lowest_valid_price(
    prices: list[ProductPrice],
    date: datetime.date,
    unit: "Unit",
    party: "Party | None",
    currency: "Currency",
) -> Decimal | None:
    valid_prices = []
    for price in prices:
        currency_factor = price.get_currency_transform_factor(currency, price.variant.product_id)
        unit_factor = price.get_unit_transform_factor(unit, price.variant.product_id)
        group_factor = price.get_party_group_transform_factor(party, price.variant.product_id)
        if (
            price.is_date_in_range(date)
            and currency_factor != 0
            and unit_factor != 0
            and group_factor != 0
        ):
            valid_prices.append(price.price * group_factor * unit_factor * currency_factor)
    if not valid_prices:
        return None
    return min(valid_prices)


def resolve_price(
    variant: "ProductVariant",
    date: datetime.date,
    unit: "Unit",
    party: "Party | None",
    currency: "Currency",
    price_list: "PriceList | None" = None,
) -> Decimal:
    """Resolve the applicable price for `variant` following the three-level
    precedence. Raises `NoPriceFound` if no level yields a match."""
    if price_list is not None:
        level_1 = list(ProductPrice.objects.filter(variant=variant, price_list=price_list))
        result = _lowest_valid_price(level_1, date, unit, party, currency)
        if result is not None:
            return result

    level_2 = list(ProductPrice.objects.filter(variant=variant, price_list__isnull=True))
    result = _lowest_valid_price(level_2, date, unit, party, currency)
    if result is not None:
        return result

    raise NoPriceFound(variant, date, party, currency, price_list)
