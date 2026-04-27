# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class ResourceManager(BaseModel):
    """Client-side model representing a resource manager."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.user = None
        super().__init__(data)
