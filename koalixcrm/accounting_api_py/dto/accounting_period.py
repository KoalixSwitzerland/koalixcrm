from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class AccountingPeriod(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.title = None
        self.begin = None
        self.end = None
        self.template_set_balance_sheet = None
        self.template_profit_loss_statement = None
        super().__init__(data)
