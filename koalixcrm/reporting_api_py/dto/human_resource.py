# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class HumanResource(BaseModel):
    """Client-side model representing a human resource."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.user = None
        self.resource_manager = None
        self.resource_type = None
        super().__init__(data)
