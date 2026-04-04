# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Work(BaseModel):
    """Client-side model representing a work entry."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.human_resource = None
        self.date = None
        self.start_time = None
        self.stop_time = None
        self.short_description = None
        self.description = None
        self.task = None
        self.reporting_period = None
        self.worked_hours = None
        super().__init__(data)
