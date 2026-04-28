# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class ReportingPeriod(BaseModel):
    """Client-side model representing a reporting period."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.project = None
        self.title = None
        self.begin = None
        self.end = None
        self.status = None
        super().__init__(data)
