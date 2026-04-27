# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class AgreementStatus(BaseModel):
    """Client-side model representing an agreement status."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.title = None
        self.description = None
        self.is_agreed = None
        super().__init__(data)
