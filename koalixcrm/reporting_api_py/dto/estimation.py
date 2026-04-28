# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Estimation(BaseModel):
    """Client-side model representing an estimation of resource consumption."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.task = None
        self.resource = None
        self.date_from = None
        self.date_until = None
        self.amount = None
        self.status = None
        self.reporting_period = None
        super().__init__(data)
