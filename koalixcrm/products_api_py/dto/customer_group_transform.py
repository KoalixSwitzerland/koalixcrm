# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class CustomerGroupTransform(BaseModel):
    """Client-side model representing a customer group transform."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.from_customer_group = None
        self.to_customer_group = None
        self.product_type = None
        self.factor = None
        super().__init__(data)
