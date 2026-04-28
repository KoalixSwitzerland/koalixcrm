# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class ProductType(BaseModel):
    """Client-side model representing a product type."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.description = None
        self.title = None
        self.product_type_identifier = None
        self.default_unit = None
        self.tax = None
        self.date_of_creation = None
        self.last_modification = None
        super().__init__(data)
