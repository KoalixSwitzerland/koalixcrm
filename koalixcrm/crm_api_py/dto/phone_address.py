# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class PhoneAddress(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.phone = None
        super().__init__(data)
