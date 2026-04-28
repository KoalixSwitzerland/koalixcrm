# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from koalixcrm.shared.base_model import BaseModel

if TYPE_CHECKING:
    from koalixcrm.shared.api_client import BaseAPIClient


class CustomerBillingCycle(BaseModel):
    """Client-side model representing a customer billing cycle."""

    def __init__(self, data: dict[str, Any], client: BaseAPIClient | None = None) -> None:
        self.name = None
        self.time_to_payment_date = None
        self.payment_reminder_time_to_payment = None
        super().__init__(data)
