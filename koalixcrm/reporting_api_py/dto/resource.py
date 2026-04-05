# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Resource(BaseModel):
    """Client-side model representing a resource."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.resource_manager = None
        self.resource_type = None
        super().__init__(data)
