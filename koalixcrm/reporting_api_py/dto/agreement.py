# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class Agreement(BaseModel):
    """Client-side model representing an agreement."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.amount = None
        self.costs = None
        self.task = None
        self.resource = None
        self.unit = None
        self.type = None
        self.status = None
        self.date_from = None
        self.date_until = None
        super().__init__(data)
