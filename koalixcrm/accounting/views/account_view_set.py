# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from koalixcrm.accounting.models import Account, AccountingPeriod
from koalixcrm.accounting.serializers.account_serializer import (
    AccountBookingSumsSerializer,
    AccountJSONSerializer,
)
from koalixcrm.shared.base_model_view_set import BaseModelViewSet


class AccountViewSet(BaseModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountJSONSerializer

    @action(detail=True, methods=["get"], url_path="booking-sums")
    def booking_sums(self, request: Request, pk: int | None = None, **kwargs: Any) -> Response:
        """Return the four booking aggregates for this account, scoped to
        the accounting period given as ``?accounting_period=<id>``.
        """
        account = self.get_object()
        period_id = request.query_params.get("accounting_period")
        if not period_id:
            raise ValidationError({"accounting_period": "query parameter is required"})
        try:
            period = AccountingPeriod.objects.get(pk=period_id)
        except AccountingPeriod.DoesNotExist:
            raise NotFound(f"AccountingPeriod {period_id} not found")
        serializer = AccountBookingSumsSerializer(account, context={"accounting_period": period})
        return Response(serializer.data)
