# -*- coding: utf-8 -*-
"""
Unit tests for koalixcrm.shared.pagination (ADR-0023 — Pagination Requires a
Total Ordering).

These tests exercise `_ordering_already_has_pk` and
`TotalOrderingPageNumberPagination._ensure_total_ordering` directly. Building
a QuerySet and reading `.query.order_by` never executes SQL (Django resolves
ordering lazily), so none of these tests need the `db` fixture.
"""
from __future__ import annotations

from django.db.models import F
from django.db.models.functions import Coalesce

from koalixcrm.accounting.models.account import Account
from koalixcrm.contracts.models.commercial_document import CommercialDocument
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.shared.pagination import (
    TotalOrderingPageNumberPagination,
    _ordering_already_has_pk,
)


class TestOrderingAlreadyHasPk:
    """Direct tests of the helper predicate."""

    def test_plain_id_field_name(self):
        assert _ordering_already_has_pk(('id',), 'id') is True

    def test_descending_id(self):
        assert _ordering_already_has_pk(('-id',), 'id') is True

    def test_pk_alias(self):
        assert _ordering_already_has_pk(('pk',), 'id') is True

    def test_descending_pk_alias(self):
        assert _ordering_already_has_pk(('-pk',), 'id') is True

    def test_pk_alias_regardless_of_actual_pk_name(self):
        # 'pk' is always a valid alias for the primary key, whatever it's
        # actually called on the model (see the multi-table-inheritance case
        # below, where the real name is 'commercialdocument_ptr').
        assert _ordering_already_has_pk(('pk',), 'commercialdocument_ptr') is True

    def test_non_id_pk_field_name_matched_by_its_real_name(self):
        assert _ordering_already_has_pk(('commercialdocument_ptr',), 'commercialdocument_ptr') is True

    def test_non_id_pk_field_name_not_matched_by_unrelated_id(self):
        # A model whose pk is not called 'id' must not be fooled by a bare
        # 'id' entry that happens to be a *different*, non-pk field.
        assert _ordering_already_has_pk(('id',), 'commercialdocument_ptr') is False

    def test_related_field_lookup_not_mistaken_for_pk(self):
        assert _ordering_already_has_pk(('party__name',), 'id') is False

    def test_descending_related_field_lookup_not_mistaken_for_pk(self):
        assert _ordering_already_has_pk(('-party__name',), 'id') is False

    def test_expression_object_ignored_not_raising(self):
        expr = F('title').desc()
        assert _ordering_already_has_pk((expr,), 'id') is False

    def test_coalesce_expression_ignored_not_raising(self):
        expr = Coalesce(F('title'), F('account_number'))
        assert _ordering_already_has_pk((expr,), 'id') is False

    def test_mixed_expression_and_pk_string(self):
        expr = F('title').desc()
        assert _ordering_already_has_pk((expr, 'pk'), 'id') is True

    def test_empty_ordering(self):
        assert _ordering_already_has_pk((), 'id') is False


class TestEnsureTotalOrdering:
    """End-to-end behaviour of `_ensure_total_ordering` on real QuerySets."""

    def test_appends_pk_when_absent(self):
        qs = Account.objects.order_by('account_number')
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        assert result.query.order_by == ('account_number', 'pk')

    def test_id_already_present_left_untouched(self):
        qs = Account.objects.order_by('id')
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        assert result.query.order_by == ('id',)

    def test_negative_id_already_present_left_untouched(self):
        qs = Account.objects.order_by('-id')
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        assert result.query.order_by == ('-id',)

    def test_pk_alias_already_present_left_untouched(self):
        qs = Account.objects.order_by('pk')
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        assert result.query.order_by == ('pk',)

    def test_falls_back_to_meta_ordering_when_query_has_none(self):
        # Account.Meta.ordering = ['account_number']; an unfiltered queryset
        # carries no query.order_by of its own until Django applies it lazily.
        qs = Account.objects.all()
        assert qs.query.order_by == ()
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        assert result.query.order_by == ('account_number', 'pk')

    def test_model_with_non_id_pk_name_uses_meta_pk_name(self):
        assert Invoice._meta.pk.name == 'commercialdocument_ptr'
        qs = Invoice.objects.order_by('commercialdocument_ptr')
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        # Already present under its real name -> untouched, no extra 'pk' appended.
        assert result.query.order_by == ('commercialdocument_ptr',)

    def test_model_with_non_id_pk_name_appends_when_absent(self):
        qs = Invoice.objects.order_by('description')
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        assert result.query.order_by == ('description', 'pk')

    def test_related_field_lookup_not_mistaken_for_pk(self):
        qs = CommercialDocument.objects.order_by('party__name')
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        assert result.query.order_by == ('party__name', 'pk')

    def test_expression_ordering_not_raising_and_pk_appended(self):
        qs = Account.objects.order_by(F('title').desc())
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        order_by = result.query.order_by
        assert len(order_by) == 2
        assert order_by[1] == 'pk'

    def test_coalesce_ordering_not_raising_and_pk_appended(self):
        qs = Account.objects.order_by(Coalesce(F('title'), F('account_number')))
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(qs)
        order_by = result.query.order_by
        assert len(order_by) == 2
        assert order_by[1] == 'pk'

    def test_non_queryset_list_passes_through_untouched(self):
        plain_list = [1, 2, 3]
        result = TotalOrderingPageNumberPagination._ensure_total_ordering(plain_list)
        assert result is plain_list

    def test_non_queryset_empty_list_passes_through_untouched(self):
        result = TotalOrderingPageNumberPagination._ensure_total_ordering([])
        assert result == []
