# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class SalesOrder(BaseModel):
    """Client-side model representing a sales order."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.party_reference = None
        self.ext_business_appl_references = {}
        self.discount = None
        self.description = None
        self.currency = None
        self.customer = None
        self.contract = None
        super().__init__(data)
