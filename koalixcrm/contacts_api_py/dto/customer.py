# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Customer(BaseModel):
    """Client-side model representing a customer."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.name = None
        self.is_lead = None
        self.default_customer_billing_cycle = None
        self.is_member_of = None
        super().__init__(data)
