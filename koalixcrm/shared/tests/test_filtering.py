# -*- coding: utf-8 -*-
"""Tests for koalixcrm.shared.filters (structural field filtering).

Two things are guarded here, and the first matters more than it looks.

`BaseModelViewSet.filter_backends` *replaces* `DEFAULT_FILTER_BACKENDS`
rather than extending it. Before this change the class listed only
`SearchFilter` and `OrderingFilter`, which meant the `DjangoFilterBackend`
configured project-wide was active on no endpoint at all — and django-filter
ignores unrecognised query parameters rather than rejecting them, so
`?product=5` returned every row in the workspace and looked like it had
worked. `TaskViewSet` had carried a `filterset_fields = ['project']` that
never did anything for exactly this reason. `test_base_viewset_*` fails if
the backend is ever dropped from that list again.
"""
from __future__ import annotations

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

from koalixcrm.products.models.product_translation import ProductTranslation
from koalixcrm.products.models.product_variant import ProductVariant
from koalixcrm.products.tests.factories.product_translation_factory import (
    StandardProductTranslationFactory,
)
from koalixcrm.products.tests.factories.product_type_factory import StandardProductTypeFactory
from koalixcrm.products.views.product_translation_view_set import ProductTranslationViewSet
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.filters import AutoFilterBackend, auto_filter_fields


class TestBaseViewSetWiring:
    """The regression guard for the silent-override trap."""

    def test_base_viewset_declares_the_filter_backend(self):
        assert AutoFilterBackend in BaseModelViewSet.filter_backends

    def test_concrete_viewset_inherits_the_filter_backend(self):
        assert AutoFilterBackend in ProductTranslationViewSet.filter_backends


class TestAutoFilterFields:
    """Which model fields become filters, derived without touching the DB."""

    def test_foreign_keys_are_filterable(self):
        fields = auto_filter_fields(ProductTranslation)
        assert 'product' in fields
        assert 'exact' in fields['product']

    def test_primary_key_supports_batch_lookup(self):
        fields = auto_filter_fields(ProductTranslation)
        assert 'in' in fields['id']

    def test_workspace_is_excluded(self):
        # Applied by the queryset and implied by the URL prefix; exposing it
        # would add a filter that can only narrow an already-narrowed list.
        assert 'workspace' not in auto_filter_fields(ProductTranslation)

    def test_identifier_char_fields_are_filterable(self):
        # `language_code` is what UC-0003 filters a product's translations
        # by; `sku`/`gtin` are what catalogue and scan flows look up. These
        # are CharFields with no `choices`, so they only work if CharField
        # is included.
        assert 'language_code' in auto_filter_fields(ProductTranslation)

        variant_fields = auto_filter_fields(ProductVariant)
        assert 'sku' in variant_fields
        assert 'gtin' in variant_fields

    def test_prose_text_fields_are_excluded(self):
        # `long_description` is a TextField: an exact match on prose is not a
        # question anyone asks. Substring search is SearchFilter's job, via
        # an explicit per-resource `search_fields`.
        assert 'long_description' not in auto_filter_fields(ProductTranslation)

    def test_no_substring_lookups_are_generated(self):
        # The cost argument that rules out auto-exposed text search: `exact`
        # is never worse than the unfiltered list, `icontains` is.
        for model_fields in (
            auto_filter_fields(ProductTranslation),
            auto_filter_fields(ProductVariant),
        ):
            for lookups in model_fields.values():
                assert not {'icontains', 'contains', 'startswith'} & set(lookups)

    def test_choice_fields_are_filterable(self):
        from koalixcrm.products.models.product import Product

        fields = auto_filter_fields(Product)
        assert 'lifecycle_status' in fields

    def test_datetime_fields_carry_range_lookups(self):
        fields = auto_filter_fields(ProductVariant)
        assert set(fields['date_of_creation']) >= {'gte', 'lte'}


@pytest.mark.django_db
class TestFilteringAppliesToListResponses:
    """End-to-end: the parameter actually narrows the queryset."""

    @staticmethod
    def _list(admin_user, query=''):
        request = APIRequestFactory().get(f'/filter-test/{query}')
        force_authenticate(request, user=admin_user)
        return ProductTranslationViewSet.as_view({'get': 'list'})(request)

    @pytest.fixture
    def admin_user(self, db):
        user, _ = User.objects.get_or_create(
            username='filter-admin',
            defaults={'email': 'filter-admin@example.com', 'is_staff': True, 'is_superuser': True},
        )
        return user

    @pytest.fixture
    def translations(self, db):
        # `StandardProductTypeFactory` has django_get_or_create on
        # `product_type_identifier`, so distinct identifiers are what make
        # these two separate rows rather than the same one twice.
        product_a = StandardProductTypeFactory.create(
            product_type_identifier='FILTER-A', title='Filterable A',
        )
        product_b = StandardProductTypeFactory.create(
            product_type_identifier='FILTER-B', title='Filterable B',
        )
        return {
            'a': StandardProductTranslationFactory.create(product=product_a, language_code='de'),
            'b': StandardProductTranslationFactory.create(product=product_b, language_code='fr'),
            'product_a': product_a,
            'product_b': product_b,
        }

    @pytest.mark.back_end_tests
    def test_unfiltered_list_returns_both_rows(self, admin_user, translations):
        response = self._list(admin_user)
        assert response.status_code == 200, response.data
        ids = {row['id'] for row in response.data['results']}
        assert {translations['a'].pk, translations['b'].pk} <= ids

    @pytest.mark.back_end_tests
    def test_foreign_key_filter_narrows_the_list(self, admin_user, translations):
        response = self._list(admin_user, f"?product={translations['product_a'].pk}")
        assert response.status_code == 200, response.data
        ids = {row['id'] for row in response.data['results']}
        assert ids == {translations['a'].pk}

    @pytest.mark.back_end_tests
    def test_list_response_is_paginated(self, admin_user, translations):
        response = self._list(admin_user)
        assert set(response.data.keys()) == {'count', 'next', 'previous', 'results'}
