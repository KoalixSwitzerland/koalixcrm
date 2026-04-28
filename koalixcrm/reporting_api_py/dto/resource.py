# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Resource(BaseModel):
    """Client-side model representing a resource."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.resource_manager = None
        self.resource_type = None
        super().__init__(data)
