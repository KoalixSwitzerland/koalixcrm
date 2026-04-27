# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class CustomerBillingCycle(BaseModel):
    """Client-side model representing a customer billing cycle."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.name = None
        self.time_to_payment_date = None
        self.payment_reminder_time_to_payment = None
        super().__init__(data)
