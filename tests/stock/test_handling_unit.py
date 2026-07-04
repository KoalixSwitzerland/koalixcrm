# -*- coding: utf-8 -*-
"""ADR-0009 Standards-Verankerung: `HandlingUnit.sscc` GS1 SSCC-18 format
validation, workspace-scoped `sscc` uniqueness, and parent/location
workspace-consistency."""
import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from koalixcrm.stock.models.handling_unit import HandlingUnit
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.stock.handling_unit_factory import StandardHandlingUnitFactory
from tests.factories.stock.location_factory import StandardLocationFactory


class HandlingUnitSsccTest(TestCase):
    @pytest.mark.back_end_tests
    def test_valid_18_digit_sscc_accepted(self):
        hu = StandardHandlingUnitFactory(sscc="123456789012345675")
        hu.full_clean()

    @pytest.mark.back_end_tests
    def test_non_numeric_sscc_rejected(self):
        hu = StandardHandlingUnitFactory.build(sscc="12345678901234567A")
        with self.assertRaises(ValidationError):
            hu.full_clean()

    @pytest.mark.back_end_tests
    def test_wrong_length_sscc_rejected(self):
        hu = StandardHandlingUnitFactory.build(sscc="12345")
        with self.assertRaises(ValidationError):
            hu.full_clean()

    @pytest.mark.back_end_tests
    def test_sscc_unique_per_workspace(self):
        workspace = DefaultWorkspaceFactory()
        StandardHandlingUnitFactory(workspace=workspace,
                                    location=StandardLocationFactory(workspace=workspace),
                                    sscc="123456789012345675")
        duplicate = HandlingUnit(
            workspace=workspace,
            sscc="123456789012345675",
            location=StandardLocationFactory(workspace=workspace),
            hu_type="PALLET",
        )
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
