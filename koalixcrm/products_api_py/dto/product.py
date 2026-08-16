# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Product(BaseModel):
    """Client-side model representing a product (renamed from `ProductType`
    — ADR-0003 Amendment 2026-06-27)."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.description = None
        self.title = None
        self.product_type_identifier = None
        self.kind = None
        self.lifecycle_status = None
        self.base_uom = None
        self.tax_class = None
        self.brand = None
        self.manufacturer_party = None
        self.country_of_origin = None
        self.product_family = None
        self.date_of_creation = None
        self.last_modification = None
        super().__init__(data)
