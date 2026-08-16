# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class ProductVariant(BaseModel):
    """Client-side model representing a sellable product variant/SKU."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.product = None
        self.sku = None
        self.gtin = None
        self.mpn = None
        self.weight_kg = None
        self.dimensions_length_m = None
        self.dimensions_width_m = None
        self.dimensions_height_m = None
        self.axis_values = None
        super().__init__(data)
