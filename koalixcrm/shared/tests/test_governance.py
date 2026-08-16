# -*- coding: utf-8 -*-
"""Tests for the ADR-0024 §2 schema/instance split.

The load-bearing test here is `test_every_governed_model_is_classified`. The
split only holds if a newly added model has to be classified deliberately; if
an unclassified model silently defaulted into the permissive class, the
governance boundary would erode exactly the way an unenforced convention
always does, and nothing would fail visibly.
"""
from __future__ import annotations

import pytest
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command

from koalixcrm.products.models.attribute_definition import AttributeDefinition
from koalixcrm.products.models.product import Product
from koalixcrm.products.models.product_variant import ProductVariant
from koalixcrm.shared.governance import (
    DATA_EDITOR_GROUP,
    SCHEMA_AUTHOR_GROUP,
    SCHEMA_MODELS,
    governed_models,
    instance_models,
    is_schema_model,
    schema_models,
    unknown_schema_entries,
)
from koalixcrm.stock.models.serial_unit import SerialUnit


class TestRegistry:
    def test_no_stale_schema_entries(self):
        assert unknown_schema_entries() == set()

    def test_every_governed_model_is_classified(self):
        governed = set(governed_models())
        classified = set(schema_models()) | set(instance_models())
        assert governed == classified

    def test_the_two_classes_are_disjoint(self):
        assert not set(schema_models()) & set(instance_models())

    def test_vocabulary_models_are_schema(self):
        assert is_schema_model(AttributeDefinition)

    def test_catalogue_data_is_not_schema(self):
        assert not is_schema_model(Product)
        assert not is_schema_model(ProductVariant)
        assert not is_schema_model(SerialUnit)

    def test_registry_is_not_vacuous(self):
        # Guards the guard: an empty registry would satisfy the disjointness
        # and classification tests above while governing nothing.
        assert len(SCHEMA_MODELS) >= 9
        assert len(instance_models()) > len(schema_models())


@pytest.mark.django_db
class TestBootstrapCommand:
    @staticmethod
    def _codenames(group: Group) -> set[str]:
        return set(group.permissions.values_list('codename', flat=True))

    @pytest.mark.back_end_tests
    def test_dry_run_writes_nothing(self):
        call_command('bootstrap_data_governance_groups', '--dry-run')
        assert not Group.objects.filter(name=SCHEMA_AUTHOR_GROUP).exists()
        assert not Group.objects.filter(name=DATA_EDITOR_GROUP).exists()

    @pytest.mark.back_end_tests
    def test_schema_authors_may_write_the_vocabulary(self):
        call_command('bootstrap_data_governance_groups')
        codenames = self._codenames(Group.objects.get(name=SCHEMA_AUTHOR_GROUP))
        assert {'add_attributedefinition', 'change_attributedefinition',
                'delete_attributedefinition'} <= codenames

    @pytest.mark.back_end_tests
    def test_data_editors_may_read_but_not_write_the_vocabulary(self):
        call_command('bootstrap_data_governance_groups')
        codenames = self._codenames(Group.objects.get(name=DATA_EDITOR_GROUP))

        assert 'view_attributedefinition' in codenames
        # The actual point of the split.
        assert 'add_attributedefinition' not in codenames
        assert 'change_attributedefinition' not in codenames
        assert 'delete_attributedefinition' not in codenames

    @pytest.mark.back_end_tests
    def test_data_editors_may_write_catalogue_data(self):
        call_command('bootstrap_data_governance_groups')
        codenames = self._codenames(Group.objects.get(name=DATA_EDITOR_GROUP))
        assert {'add_product', 'change_product', 'add_productvariant'} <= codenames

    @pytest.mark.back_end_tests
    def test_no_schema_write_permission_leaks_into_the_editor_group(self):
        call_command('bootstrap_data_governance_groups')
        codenames = self._codenames(Group.objects.get(name=DATA_EDITOR_GROUP))
        forbidden = {
            f'{action}_{model_name}'
            for _, model_name in SCHEMA_MODELS
            for action in ('add', 'change', 'delete')
        }
        assert not (codenames & forbidden)

    @pytest.mark.back_end_tests
    def test_rerun_converges_rather_than_accumulates(self):
        call_command('bootstrap_data_governance_groups')
        editors = Group.objects.get(name=DATA_EDITOR_GROUP)
        before = self._codenames(editors)

        # A permission granted out of band must be revoked on the next run,
        # otherwise the group drifts permissive over time.
        editors.permissions.add(
            Permission.objects.get(codename='add_attributedefinition')
        )
        call_command('bootstrap_data_governance_groups')

        assert self._codenames(Group.objects.get(name=DATA_EDITOR_GROUP)) == before
