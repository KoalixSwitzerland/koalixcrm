# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class CurrencyTransform(BaseModel):
    """Client-side model representing a currency transform."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.from_currency = None
        self.to_currency = None
        self.product_type = None
        self.factor = None
        super().__init__(data)
