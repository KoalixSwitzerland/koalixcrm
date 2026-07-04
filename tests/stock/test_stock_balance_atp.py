# -*- coding: utf-8 -*-
"""REQ-0020 / ADR-0010: six-segment StockBalance arithmetic + ATP formula
ATP = qty_on_hand - qty_booked - qty_reserved_for_document + qty_ordered."""
from decimal import Decimal

import pytest
from django.test import TestCase

from tests.factories.stock.stock_balance_factory import StandardStockBalanceFactory


class StockBalanceAtpTest(TestCase):
    @pytest.mark.back_end_tests
    def test_atp_formula(self):
        balance = StandardStockBalanceFactory(
            qty_on_hand=Decimal("100"),
            qty_booked=Decimal("10"),
            qty_reserved_for_document=Decimal("15"),
            qty_ordered=Decimal("30"),
            qty_in_transit=Decimal("999"),
            qty_quarantine=Decimal("999"),
        )
        self.assertEqual(balance.atp, Decimal("105"))

    @pytest.mark.back_end_tests
    def test_in_transit_and_quarantine_excluded_from_atp(self):
        balance = StandardStockBalanceFactory(
            qty_on_hand=Decimal("50"),
            qty_in_transit=Decimal("1000"),
            qty_quarantine=Decimal("1000"),
        )
        self.assertEqual(balance.atp, Decimal("50"))

    @pytest.mark.back_end_tests
    def test_negative_segments_are_rejected(self):
        from django.core.exceptions import ValidationError

        balance = StandardStockBalanceFactory.build(qty_on_hand=Decimal("-1"))
        with self.assertRaises(ValidationError):
            balance.full_clean()
