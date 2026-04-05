# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Estimation(BaseModel):
    """Client-side model representing an estimation of resource consumption."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.task = None
        self.resource = None
        self.date_from = None
        self.date_until = None
        self.amount = None
        self.status = None
        self.reporting_period = None
        super().__init__(data)
