# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Invoice(BaseModel):
    """Client-side model representing an invoice."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.payable_until = None
        self.payment_bank_reference = None
        self.status = None
        self.external_reference = None
        self.discount = None
        self.description = None
        self.currency = None
        self.customer = None
        self.contract = None
        super().__init__(data)
