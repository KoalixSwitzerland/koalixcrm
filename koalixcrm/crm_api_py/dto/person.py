# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Person(BaseModel):
    """Client-side model representing a person."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.prefix = None
        self.name = None
        self.pre_name = None
        self.email = None
        self.phone = None
        self.role = None
        super().__init__(data)
