# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Project(BaseModel):
    """Client-side model representing a project."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.project_name = None
        self.description = None
        self.project_manager = None
        self.default_currency = None
        self.project_status = None
        self.date_of_creation = None
        self.last_modification = None
        super().__init__(data)
