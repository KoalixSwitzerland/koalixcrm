# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class DespatchAdvice(BaseModel):
    """Client-side model representing a despatch advice."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.tracking_reference = None
        self.status = None
        self.external_reference = None
        self.discount = None
        self.description = None
        self.currency = None
        self.customer = None
        self.contract = None
        super().__init__(data)
