# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class Product(BaseModel):
    """Client-side model representing a product."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.identifier = None
        self.product_type = None
        super().__init__(data)
