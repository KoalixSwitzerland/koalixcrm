# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class ReportingPeriod(BaseModel):
    """Client-side model representing a reporting period."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.project = None
        self.title = None
        self.begin = None
        self.end = None
        self.status = None
        super().__init__(data)
