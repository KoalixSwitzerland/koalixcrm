# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class DespatchAdvice(BaseModel):
    """Client-side model representing a despatch advice."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.tracking_reference = None
        self.status = None
        self.party_reference = None
        self.ext_business_appl_references = {}
        self.discount = None
        self.description = None
        self.currency = None
        self.customer = None
        self.contract = None
        super().__init__(data)
