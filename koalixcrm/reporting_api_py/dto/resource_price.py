# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class ResourcePrice(BaseModel):
    """Client-side model representing a resource price."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.resource = None
        self.price = None
        self.currency = None
        self.unit = None
        self.customer_group = None
        self.valid_from = None
        self.valid_until = None
        super().__init__(data)
