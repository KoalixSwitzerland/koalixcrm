# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class PaymentReminder(BaseModel):
    """Client-side model representing a payment reminder."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.payable_until = None
        self.payment_bank_reference = None
        self.iteration_number = None
        self.status = None
        self.party_reference = None
        self.ext_business_appl_references = {}
        self.discount = None
        self.description = None
        self.currency = None
        self.customer = None
        self.contract = None
        super().__init__(data)
