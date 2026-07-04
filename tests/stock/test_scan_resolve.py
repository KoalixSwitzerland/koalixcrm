# -*- coding: utf-8 -*-
"""ADR-0016: scan-resolve service tests — each identifier type, GS1-beats-
free-text precedence, free-text multi-hit 409, cross-workspace isolation,
and catalog-wide GTIN resolution."""
import pytest
from django.test import TestCase

from koalixcrm.stock.services import scan_resolve
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_variant_factory import StandardProductVariantFactory
from tests.factories.stock.handling_unit_factory import StandardHandlingUnitFactory
from tests.factories.stock.location_factory import StandardLocationFactory
from tests.factories.stock.serial_unit_factory import StandardSerialUnitFactory


class ScanResolveTest(TestCase):
    def setUp(self):
        self.workspace = DefaultWorkspaceFactory()
        self.other_workspace = DefaultWorkspaceFactory(name="Other Workspace")

    @pytest.mark.back_end_tests
    def test_resolve_location_by_gln(self):
        location = StandardLocationFactory(workspace=self.workspace, external_ref="1234567890128")
        match = scan_resolve.resolve("(414)1234567890128", workspace=self.workspace)
        self.assertEqual(match.kind, "location")
        self.assertEqual(match.id, location.pk)
        self.assertEqual(match.matched_field, "external_ref")

    @pytest.mark.back_end_tests
    def test_resolve_handling_unit_by_sscc(self):
        handling_unit = StandardHandlingUnitFactory(workspace=self.workspace, sscc="123456789012345675")
        match = scan_resolve.resolve("(00)123456789012345675", workspace=self.workspace)
        self.assertEqual(match.kind, "handling_unit")
        self.assertEqual(match.id, handling_unit.pk)

    @pytest.mark.back_end_tests
    def test_resolve_serial_unit_by_sgtin(self):
        unit = StandardSerialUnitFactory(workspace=self.workspace, global_uid="000042")
        match = scan_resolve.resolve("(01)04012345123456(21)000042", workspace=self.workspace)
        self.assertEqual(match.kind, "serial_unit")
        self.assertEqual(match.id, unit.pk)

    @pytest.mark.back_end_tests
    def test_resolve_serial_unit_by_giai(self):
        unit = StandardSerialUnitFactory(workspace=self.workspace, global_uid="GIAI-VALUE-1", serial_number="SN-GIAI")
        match = scan_resolve.resolve("(8003)GIAI-VALUE-1", workspace=self.workspace)
        self.assertEqual(match.kind, "serial_unit")
        self.assertEqual(match.id, unit.pk)

    @pytest.mark.back_end_tests
    def test_resolve_product_variant_by_gtin_is_catalog_wide(self):
        variant = StandardProductVariantFactory(
            workspace=self.other_workspace, sku="GTIN-VARIANT", gtin="99999999999999",
        )
        # Resolved from self.workspace even though the variant belongs to other_workspace.
        match = scan_resolve.resolve("(01)99999999999999", workspace=self.workspace)
        self.assertEqual(match.kind, "product_variant")
        self.assertEqual(match.id, variant.pk)

    @pytest.mark.back_end_tests
    def test_gs1_beats_free_text(self):
        """A code that both parses as a GS1 GLN and would also free-text
        match a SerialUnit.global_uid resolves via the GS1 path."""
        location = StandardLocationFactory(workspace=self.workspace, external_ref="9999999999999")
        gs1_code = "(414)9999999999999"
        StandardSerialUnitFactory(workspace=self.workspace, global_uid=gs1_code)
        match = scan_resolve.resolve(gs1_code, workspace=self.workspace)
        self.assertEqual(match.kind, "location")
        self.assertEqual(match.id, location.pk)

    @pytest.mark.back_end_tests
    def test_free_text_sku_match(self):
        variant = StandardProductVariantFactory(workspace=self.workspace, sku="FREETEXT-SKU-1")
        match = scan_resolve.resolve("FREETEXT-SKU-1", workspace=self.workspace)
        self.assertEqual(match.kind, "product_variant")
        self.assertEqual(match.id, variant.pk)
        self.assertEqual(match.matched_field, "sku")

    @pytest.mark.back_end_tests
    def test_free_text_multi_hit_raises_409_equivalent(self):
        code = "AMBIGUOUS-CODE"
        StandardLocationFactory(workspace=self.workspace, external_ref=code)
        StandardSerialUnitFactory(workspace=self.workspace, global_uid=code)
        with self.assertRaises(scan_resolve.ScanMultipleMatches) as ctx:
            scan_resolve.resolve(code, workspace=self.workspace)
        self.assertEqual(len(ctx.exception.candidates), 2)

    @pytest.mark.back_end_tests
    def test_no_match_raises_not_found(self):
        with self.assertRaises(scan_resolve.ScanNotFound):
            scan_resolve.resolve("NO-SUCH-CODE", workspace=self.workspace)

    @pytest.mark.back_end_tests
    def test_cross_workspace_isolation_for_free_text(self):
        StandardLocationFactory(workspace=self.other_workspace, external_ref="ISOLATED-CODE")
        with self.assertRaises(scan_resolve.ScanNotFound):
            scan_resolve.resolve("ISOLATED-CODE", workspace=self.workspace)

    @pytest.mark.back_end_tests
    def test_cross_workspace_isolation_for_sscc(self):
        other_location = StandardLocationFactory(workspace=self.other_workspace, code="OTHER-LOC")
        StandardHandlingUnitFactory(
            workspace=self.other_workspace, sscc="123456789012345675", location=other_location,
        )
        with self.assertRaises(scan_resolve.ScanNotFound):
            scan_resolve.resolve("(00)123456789012345675", workspace=self.workspace)
