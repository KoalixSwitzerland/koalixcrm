# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class Quotation(BaseModel):
    """Client-side model representing a quotation."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.valid_until = None
        self.status = None
        self.external_reference = None
        self.discount = None
        self.description = None
        self.currency = None
        self.customer = None
        self.contract = None
        super().__init__(data)
