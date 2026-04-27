# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class Position(BaseModel):
    """Client-side model representing a position."""

    def __init__(self, data: Dict[str, Any], client=None):
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
        super().__init__(data)
