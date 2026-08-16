# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class ProductMedia(BaseModel):
    """Client-side model representing a product/variant media reference."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.product = None
        self.variant = None
        self.media_type = None
        self.object_key = None
        super().__init__(data)
