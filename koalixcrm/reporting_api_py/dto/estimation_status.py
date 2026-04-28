# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class EstimationStatus(BaseModel):
    """Client-side model representing an estimation status."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.title = None
        self.description = None
        self.is_obsolete = None
        super().__init__(data)
