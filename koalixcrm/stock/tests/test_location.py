# -*- coding: utf-8 -*-
"""REQ-0018: `Location` n-level hierarchy — type ordering, cycle rejection,
workspace-cross-parent rejection, code/external_ref uniqueness, breadcrumb
path traversal."""
import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from koalixcrm.stock.models.choices import LocationType
from koalixcrm.stock.models.location import Location
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.stock.tests.factories.location_factory import StandardLocationFactory


class LocationHierarchyTest(TestCase):
    @pytest.mark.back_end_tests
    def test_root_location_without_parent_is_valid(self):
        root = StandardLocationFactory(code="ROOT", location_type=LocationType.WAREHOUSE)
        root.full_clean()
        self.assertIsNone(root.parent)

    @pytest.mark.back_end_tests
    def test_four_level_hierarchy_and_breadcrumb_path(self):
        rack = StandardLocationFactory(code="RACK-1", location_type=LocationType.RACK)
        shelf = StandardLocationFactory(code="SHELF-1", location_type=LocationType.SHELF, parent=rack)
        layer = StandardLocationFactory(code="LAYER-1", location_type=LocationType.LAYER, parent=shelf)
        bin_ = StandardLocationFactory(code="BIN-1", location_type=LocationType.BIN, parent=layer)

        path = bin_.get_ancestor_path()
        self.assertEqual([loc.code for loc in path], ["RACK-1", "SHELF-1", "LAYER-1", "BIN-1"])

    @pytest.mark.back_end_tests
    def test_direct_self_parent_rejected(self):
        loc = StandardLocationFactory(code="SELF-1")
        loc.parent_id = loc.pk
        with self.assertRaises(ValidationError):
            loc.full_clean()

    @pytest.mark.back_end_tests
    def test_transitive_cycle_rejected(self):
        a = StandardLocationFactory(code="A")
        b = StandardLocationFactory(code="B", parent=a)
        c = StandardLocationFactory(code="C", parent=b)
        # a -> c would close the cycle a -> c -> b -> a
        a.parent = c
        with self.assertRaises(ValidationError):
            a.full_clean()

    @pytest.mark.back_end_tests
    def test_parent_from_other_workspace_rejected(self):
        other_workspace = DefaultWorkspaceFactory(name="Other Workspace")
        foreign_parent = StandardLocationFactory(code="FOREIGN", workspace=other_workspace)
        child = Location(
            workspace=DefaultWorkspaceFactory(),
            location_type=LocationType.BIN,
            code="CHILD",
            name="Child",
            parent=foreign_parent,
        )
        with self.assertRaises(ValidationError):
            child.full_clean()

    @pytest.mark.back_end_tests
    def test_code_unique_per_workspace(self):
        workspace = DefaultWorkspaceFactory()
        StandardLocationFactory(code="DUP", workspace=workspace)
        duplicate = Location(
            workspace=workspace,
            location_type=LocationType.WAREHOUSE,
            code="DUP",
            name="Duplicate",
        )
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    @pytest.mark.back_end_tests
    def test_inactive_location_remains_traversable(self):
        rack = StandardLocationFactory(code="RACK-2")
        bin_ = StandardLocationFactory(code="BIN-2", parent=rack, is_active=False)
        path = bin_.get_ancestor_path()
        self.assertEqual([loc.code for loc in path], ["RACK-2", "BIN-2"])
