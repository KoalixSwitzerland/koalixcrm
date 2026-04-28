# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Price(BaseModel):
    """Client-side model representing a price."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.unit = None
        self.currency = None
        self.customer_group = None
        self.price = None
        self.valid_from = None
        self.valid_until = None
        super().__init__(data)
