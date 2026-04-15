# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Tax(BaseModel):
    """Client-side model representing a tax."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.tax_rate = None
        self.name = None
        self.account_activa = None
        self.account_passiva = None
        super().__init__(data)
