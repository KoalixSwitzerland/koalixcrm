from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class Booking(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
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
