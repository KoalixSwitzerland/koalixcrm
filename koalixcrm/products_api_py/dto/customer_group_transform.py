# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class CustomerGroupTransform(BaseModel):
    """Client-side model for CustomerGroupTransform (post-v2.0.0 Party shape).

    Note: the model class is still named `CustomerGroupTransform` because it
    carries the product-pricing semantics of the legacy field, but it now
    references `party_group` on both sides.
    """

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.from_party_group = None
        self.to_party_group = None
        self.product_type = None
        self.factor = None
        super().__init__(data)
