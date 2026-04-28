# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Contract(BaseModel):
    """Client-side model representing a contract (post-v2.0.0 Party shape)."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.description = None
        self.buyer_party = None
        self.supplier_party = None
        self.default_currency = None
        self.default_template_set = None
        self.date_of_creation = None
        self.last_modification = None
        super().__init__(data)
