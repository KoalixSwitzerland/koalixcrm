# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Project(BaseModel):
    """Client-side model representing a project."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.project_name = None
        self.description = None
        self.project_manager = None
        self.default_currency = None
        self.project_status = None
        self.date_of_creation = None
        self.last_modification = None
        super().__init__(data)
