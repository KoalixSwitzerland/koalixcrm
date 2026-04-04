# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Supplier(BaseModel):
    """Client-side model representing a supplier."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.name = None
        self.offers_shipment_to_customers = None
        super().__init__(data)
