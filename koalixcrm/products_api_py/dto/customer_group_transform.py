# -*- coding: utf-8 -*-
from typing import Any, Dict

from koalixcrm.shared.base_model import BaseModel


class CustomerGroupTransform(BaseModel):
    """Client-side model for CustomerGroupTransform (post-v2.0.0 Party shape).

    Note: the model class is still named `CustomerGroupTransform` because it
    carries the product-pricing semantics of the legacy field, but it now
    references `party_group` on both sides.
    """

    def __init__(self, data: Dict[str, Any], client=None):
        self.from_party_group = None
        self.to_party_group = None
        self.product_type = None
        self.factor = None
        super().__init__(data)
