# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class CurrencyTransform(BaseModel):
    """Client-side model representing a currency transform."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.from_currency = None
        self.to_currency = None
        self.product_type = None
        self.factor = None
        super().__init__(data)
