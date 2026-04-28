# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class GenericProjectLink(BaseModel):
    """Client-side model representing a generic project link."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.project = None
        self.project_link_type = None
        self.content_type = None
        self.object_id = None
        self.date_of_creation = None
        self.last_modified_by = None
        super().__init__(data)
