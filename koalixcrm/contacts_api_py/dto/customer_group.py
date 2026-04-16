# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class CustomerGroup(BaseModel):
    """Client-side model representing a customer group."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.name = None
        super().__init__(data)
