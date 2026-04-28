# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class CommercialDocumentPosition(BaseModel):
    """Client-side model representing a commercial document position."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.position_number = None
        self.quantity = None
        self.description = None
        self.discount = None
        self.product_type = None
        self.unit = None
        self.sent_on = None
        self.overwrite_product_price = None
        self.position_price_per_unit = None
        self.last_pricing_date = None
        self.last_calculated_price = None
        self.last_calculated_tax = None
        self.commercial_document = None
        super().__init__(data)
