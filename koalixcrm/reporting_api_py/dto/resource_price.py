# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class ResourcePrice(BaseModel):
    """Client-side model representing a resource price."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.resource = None
        self.price = None
        self.currency = None
        self.unit = None
        self.customer_group = None
        self.valid_from = None
        self.valid_until = None
        super().__init__(data)
