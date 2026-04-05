from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class Account(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.account_number = None
        self.title = None
        self.account_type = None
        self.description = None
        self.is_open_reliabilities_account = None
        self.is_open_interest_account = None
        self.is_product_inventory_activa = None
        self.is_a_customer_payment_account = None
        super().__init__(data)
