# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class EstimationStatus(BaseModel):
    """Client-side model representing an estimation status."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.title = None
        self.description = None
        self.is_obsolete = None
        super().__init__(data)
