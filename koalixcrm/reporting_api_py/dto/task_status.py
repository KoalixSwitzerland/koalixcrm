# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class TaskStatus(BaseModel):
    """Client-side model representing a task status."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.title = None
        self.description = None
        self.is_done = None
        super().__init__(data)
