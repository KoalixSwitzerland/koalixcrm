# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Work(BaseModel):
    """Client-side model representing a work entry."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.human_resource = None
        self.date = None
        self.start_time = None
        self.stop_time = None
        self.short_description = None
        self.description = None
        self.task = None
        self.reporting_period = None
        self.worked_hours = None
        super().__init__(data)
