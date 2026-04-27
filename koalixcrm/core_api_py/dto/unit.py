# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class Unit(BaseModel):
    """Client-side model representing a unit."""

    def __init__(self, data: Dict[str, Any], client=None):
        self.description = None
        self.short_name = None
        self.is_a_fraction_of = None
        self.fraction_factor_to_next_higher_unit = None
        super().__init__(data)
