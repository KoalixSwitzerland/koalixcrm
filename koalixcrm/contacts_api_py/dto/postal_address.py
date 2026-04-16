# -*- coding: utf-8 -*-
from typing import Dict, Any
from koalixcrm.shared.base_model import BaseModel


class PostalAddress(BaseModel):
    def __init__(self, data: Dict[str, Any], client=None):
        self.prefix = None
        self.name = None
        self.pre_name = None
        self.address_line_1 = None
        self.address_line_2 = None
        self.address_line_3 = None
        self.address_line_4 = None
        self.zip_code = None
        self.town = None
        self.state = None
        self.country = None
        super().__init__(data)
