# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Unit(BaseModel):
    """Client-side model representing a unit."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.description = None
        self.short_name = None
        self.is_a_fraction_of = None
        self.fraction_factor_to_next_higher_unit = None
        super().__init__(data)
