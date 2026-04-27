from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class ProductCategory(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.title = None
        self.profit_account = None
        self.loss_account = None
        super().__init__(data)
