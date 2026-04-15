# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class UnitTransform(BaseModel):
    """Client-side model representing a unit transform."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.from_unit = None
        self.to_unit = None
        self.product_type = None
        self.factor = None
        super().__init__(data)
