from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class AccountingPeriod(BaseModel):
    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.title = None
        self.begin = None
        self.end = None
        self.template_set_balance_sheet = None
        self.template_profit_loss_statement = None
        super().__init__(data)
