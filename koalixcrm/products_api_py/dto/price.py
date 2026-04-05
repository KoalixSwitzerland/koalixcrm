# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Price(BaseModel):
    """Client-side model representing a price."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.unit = None
        self.currency = None
        self.customer_group = None
        self.price = None
        self.valid_from = None
        self.valid_until = None
        super().__init__(data)
