# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class AgreementType(BaseModel):
    """Client-side model representing an agreement type."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.title = None
        self.description = None
        super().__init__(data)
