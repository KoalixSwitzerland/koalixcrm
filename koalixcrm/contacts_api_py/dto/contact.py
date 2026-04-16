# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Contact(BaseModel):
    """Client-side model representing a contact."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.name = None
        self.date_of_creation = None
        self.last_modification = None
        self.last_modified_by = None
        super().__init__(data)
