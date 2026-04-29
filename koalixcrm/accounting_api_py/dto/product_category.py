from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class ProductCategory(BaseModel):
    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.title = None
        self.profit_account = None
        self.loss_account = None
        super().__init__(data)
