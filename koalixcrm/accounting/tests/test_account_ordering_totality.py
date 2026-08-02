# -*- coding: utf-8 -*-
"""
ADR-0023 regression test for AccountViewSet.

Account.Meta.ordering = ['account_number'] is not unique — several accounts
can share the same account_number — so this is exactly the kind of ViewSet
the ADR is about: pagination is safe to page-walk only because
TotalOrderingPageNumberPagination appends the primary key as a tiebreaker.

Uses the plain ORM (not StandardAccountFactory) to create the tie group,
because StandardAccountFactory's `django_get_or_create = ('account_number',)`
would collapse same-account_number rows into one instead of creating
distinct, tied rows.
"""
from __future__ import annotations

from koalixcrm.accounting.models.account import Account
from koalixcrm.accounting.views.account_view_set import AccountViewSet
from koalixcrm.shared.tests.ordering_totality import OrderingTotalityTestCaseMixin


class TestAccountOrderingTotality(OrderingTotalityTestCaseMixin):
    viewset_class = AccountViewSet
    pagination_page_size = 3
    tie_group_size = 7

    @staticmethod
    def create_tied_rows(count):
        return [
            Account.objects.create(
                account_number=4000,  # identical for every row -> genuine tie group
                title=f"Tied Account {i}",
                account_type="A",
                description="Created for ADR-0023 ordering totality test",
                is_open_reliabilities_account=False,
                is_open_interest_account=False,
                is_product_inventory_activa=False,
                is_a_customer_payment_account=False,
            )
            for i in range(count)
        ]
