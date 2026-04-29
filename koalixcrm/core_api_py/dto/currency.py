# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Currency(BaseModel):
    """Client-side model representing a currency."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.description = None
        self.short_name = None
        self.rounding = None
        super().__init__(data)
