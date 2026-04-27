# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class GenericTaskLink(BaseModel):
    """Client-side model representing a generic task link."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.task = None
        self.task_link_type = None
        self.content_type = None
        self.object_id = None
        self.date_of_creation = None
        self.last_modified_by = None
        super().__init__(data)
