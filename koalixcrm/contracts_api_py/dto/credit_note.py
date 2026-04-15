# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class CreditNote(BaseModel):
    """Client-side model representing a credit note."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.corrects_invoice = None
        self.status = None
        self.issue_date = None
        self.reason = None
        self.external_reference = None
        self.discount = None
        self.description = None
        self.currency = None
        self.customer = None
        self.contract = None
        self.date_of_creation = None
        self.last_modification = None
        super().__init__(data)
