# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Task(BaseModel):
    """Client-side model representing a task."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.title = None
        self.description = None
        self.project = None
        self.status = None
        self.last_status_change = None
        super().__init__(data)
