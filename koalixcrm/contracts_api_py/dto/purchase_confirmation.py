# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class PurchaseConfirmation(BaseModel):
    """Client-side model representing a purchase confirmation."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.external_reference = None
        self.discount = None
        self.description = None
        self.currency = None
        self.customer = None
        self.contract = None
        super().__init__(data)
