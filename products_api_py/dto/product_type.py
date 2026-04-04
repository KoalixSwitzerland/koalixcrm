# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class ProductType(BaseModel):
    """Client-side model representing a product type."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.description = None
        self.title = None
        self.product_type_identifier = None
        self.default_unit = None
        self.tax = None
        self.date_of_creation = None
        self.last_modification = None
        super().__init__(data)
