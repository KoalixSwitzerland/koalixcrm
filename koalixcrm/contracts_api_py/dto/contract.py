# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class Contract(BaseModel):
    """Client-side model representing a contract (post-v2.0.0 Party shape)."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.description = None
        self.buyer_party = None
        self.supplier_party = None
        self.default_currency = None
        self.default_template_set = None
        self.date_of_creation = None
        self.last_modification = None
        super().__init__(data)
