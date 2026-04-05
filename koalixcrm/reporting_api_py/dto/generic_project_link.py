# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class GenericProjectLink(BaseModel):
    """Client-side model representing a generic project link."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.project = None
        self.project_link_type = None
        self.content_type = None
        self.object_id = None
        self.date_of_creation = None
        self.last_modified_by = None
        super().__init__(data)
