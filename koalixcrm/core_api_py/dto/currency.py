# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Currency(BaseModel):
    """Client-side model representing a currency."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.description = None
        self.short_name = None
        self.rounding = None
        super().__init__(data)
