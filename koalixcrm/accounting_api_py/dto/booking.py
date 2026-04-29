from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class Booking(BaseModel):
    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.from_account = None
        self.to_account = None
        self.amount = None
        self.description = None
        self.booking_reference = None
        self.booking_date = None
        self.accounting_period = None
        self.staff = None
        self.date_of_creation = None
        self.last_modification = None
        self.last_modified_by = None
        super().__init__(data)
