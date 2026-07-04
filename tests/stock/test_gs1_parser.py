# -*- coding: utf-8 -*-
"""ADR-0016: GS1 Application Identifier element-string parser unit tests."""
import pytest
from django.test import SimpleTestCase

from koalixcrm.stock.services import gs1_parser


class GS1ParserTest(SimpleTestCase):
    @pytest.mark.back_end_tests
    def test_gtin_only(self):
        result = gs1_parser.parse("(01)04012345123456")
        self.assertEqual(result.gtin, "04012345123456")
        self.assertIsNone(result.serial)
        self.assertFalse(result.is_sgtin)

    @pytest.mark.back_end_tests
    def test_sgtin_gtin_plus_serial(self):
        result = gs1_parser.parse("(01)04012345123456(21)000001")
        self.assertEqual(result.gtin, "04012345123456")
        self.assertEqual(result.serial, "000001")
        self.assertTrue(result.is_sgtin)

    @pytest.mark.back_end_tests
    def test_sscc(self):
        result = gs1_parser.parse("(00)123456789012345675")
        self.assertEqual(result.sscc, "123456789012345675")

    @pytest.mark.back_end_tests
    def test_giai(self):
        result = gs1_parser.parse("(8003)0" + "1" * 17)
        self.assertIsNotNone(result.giai)

    @pytest.mark.back_end_tests
    def test_gln(self):
        result = gs1_parser.parse("(414)1234567890128")
        self.assertEqual(result.gln, "1234567890128")

    @pytest.mark.back_end_tests
    def test_free_text_is_not_matched(self):
        result = gs1_parser.parse("SHELF-A-01")
        self.assertFalse(result.matched)

    @pytest.mark.back_end_tests
    def test_unbracketed_gtin(self):
        result = gs1_parser.parse("01" + "0" * 14)
        self.assertEqual(result.gtin, "0" * 14)
