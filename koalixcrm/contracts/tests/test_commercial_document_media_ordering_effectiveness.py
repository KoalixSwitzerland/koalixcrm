# -*- coding: utf-8 -*-
"""
ADR-0023 effectiveness test for CommercialDocumentMediaViewSet.

CommercialDocumentMediaViewSet is deliberately picked because it is the
weakest case in the codebase: it does not inherit BaseModelViewSet (no
OrderingFilter, no SearchFilter), it does not declare `ordering` or
`ordering_fields` anywhere, and `get_queryset()` returns a bare
`CommercialDocumentMedia.objects.all()` / `.filter(workspace=...)` with no
`.order_by()` call of its own. Whatever total-ordering guarantee this
ViewSet has can only come from the pagination class — there is nothing else
in the ViewSet for it to come from. `Meta.ordering = ['-created_at']` on the
model is itself non-unique (see koalixcrm/contracts/models/commercial_document_media.py).

Three things are asserted, corresponding to the three ways a "the mechanism
works" test can go wrong:

1. **Structural assertion** (`test_paginate_queryset_final_ordering_resolves_to_pk`):
   capture the queryset `paginate_queryset` actually pages over and assert
   its final ordering entry resolves to the primary key. This does not
   depend on tie-break behaviour happening to come out a particular way on
   SQLite, so it cannot pass by accident the way a purely behavioural tie
   test can (see ADR-0023 Notes and the module-level warning in
   koalixcrm/shared/tests/ordering_totality.py's docstring history).

2. **Behavioural effectiveness** (`TestCommercialDocumentMediaOrderingTotality`,
   via `OrderingTotalityTestCaseMixin`): a full page walk over a real tie
   group (identical `created_at`, forced via `.update()` since
   `auto_now_add` would otherwise make an exact SQLite-level tie a matter of
   timing luck) returns every row exactly once.

3. **Known limitation, not proof of a fix** (`test_offset_shift_still_produces_a_duplicate`):
   the ADR explicitly does not claim to fix offset shift (a row inserted
   ahead of the page boundary mid-walk). This test reproduces that failure
   mode on purpose, to keep it from ever being mistaken for something the
   tiebreaker mechanism prevents. `BaseAPIClient._get_object_list`
   deduplicates by id for exactly this reason.
"""
from __future__ import annotations

import datetime

from rest_framework.test import APIRequestFactory, force_authenticate

from koalixcrm.contracts.models.commercial_document_media import (
    CommercialDocumentMedia,
)
from koalixcrm.contracts.tests.factories.commercial_document_factory import (
    StandardCommercialDocumentFactory,
)
from koalixcrm.contracts.views.commercial_document_media_view_set import (
    CommercialDocumentMediaViewSet,
)
from koalixcrm.shared.pagination import TotalOrderingPageNumberPagination
from koalixcrm.shared.tests.ordering_totality import OrderingTotalityTestCaseMixin


def _create_tied_media(count, commercial_document):
    """Create `count` CommercialDocumentMedia rows with an identical
    created_at, so they are a genuine tie under Meta.ordering = ['-created_at'].

    `.update()` is used because `auto_now_add` re-derives the timestamp on
    every `.save()`/`.create()`, so passing `created_at=...` to `create()`
    would be silently ignored.
    """
    rows = [
        CommercialDocumentMedia.objects.create(
            workspace=commercial_document.workspace,
            commercial_document=commercial_document,
            s3_url=f"https://example-bucket.invalid/media-{i}.pdf",
            s3_key=f"media-{i}.pdf",
            status="completed",
            media_type="application/pdf",
        )
        for i in range(count)
    ]
    tie_time = rows[0].created_at
    CommercialDocumentMedia.objects.filter(pk__in=[row.pk for row in rows]).update(created_at=tie_time)
    for row in rows:
        row.refresh_from_db()
    return rows


class TestCommercialDocumentMediaOrderingTotality(OrderingTotalityTestCaseMixin):
    """Behavioural effectiveness test (point 2 above), via the reusable mixin."""

    viewset_class = CommercialDocumentMediaViewSet
    pagination_page_size = 3
    tie_group_size = 7

    @staticmethod
    def create_tied_rows(count):
        commercial_document = StandardCommercialDocumentFactory.create()
        return _create_tied_media(count, commercial_document)


class TestPaginateQuerysetStructuralOrdering:
    """Point 1: a structural assertion that cannot pass by accident on any
    database backend, because it never relies on how tied rows happen to
    come back from a real query — it inspects the ordering clause itself.
    """

    def test_paginate_queryset_final_ordering_resolves_to_pk(self, db):
        """Goes through the real `paginate_queryset()` call, not
        `_ensure_total_ordering()` in isolation.

        Calling `_ensure_total_ordering` directly would only prove the helper
        is correct, not that `paginate_queryset` actually calls it -- exactly
        the wiring that breaks if the call inside `paginate_queryset` is ever
        removed or short-circuited. `PageNumberPagination.paginate_queryset`
        (the base class) is monkeypatched to record the queryset it is
        handed, then delegates to the real, unmodified base-class
        implementation, so this exercises the genuine code path end to end,
        including the actual DB round trip.
        """
        from unittest import mock

        from rest_framework.pagination import PageNumberPagination
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory

        commercial_document = StandardCommercialDocumentFactory.create()
        _create_tied_media(3, commercial_document)

        # get_queryset() on this ViewSet returns .all() unordered, exactly
        # as it does at request time for a superuser.
        base_queryset = CommercialDocumentMediaViewSet.queryset.all()
        assert base_queryset.query.order_by == (), (
            "test premise broken: the ViewSet's base queryset already carries "
            "an explicit order_by, so this is no longer testing the fallback path"
        )

        captured: dict = {}
        real_base_paginate_queryset = PageNumberPagination.paginate_queryset

        def _capturing_paginate_queryset(self, queryset, request, view=None):
            captured["order_by"] = queryset.query.order_by
            return real_base_paginate_queryset(self, queryset, request, view=view)

        pagination_class = type(
            "_StructuralAssertionPagination", (TotalOrderingPageNumberPagination,), {"page_size": 2}
        )
        paginator = pagination_class()
        request = Request(APIRequestFactory().get("/ordering-totality-test/?page=1"))

        with mock.patch.object(PageNumberPagination, "paginate_queryset", _capturing_paginate_queryset):
            paginator.paginate_queryset(base_queryset, request, view=None)

        assert "order_by" in captured, "paginate_queryset was not called at all"
        order_by = captured["order_by"]

        assert order_by, "expected a non-empty effective ordering to reach DRF's paginate_queryset"
        final_entry = order_by[-1]
        assert isinstance(final_entry, str), f"final ordering entry is not a plain field reference: {final_entry!r}"
        pk_name = CommercialDocumentMedia._meta.pk.name
        assert final_entry.removeprefix("-") in ("pk", pk_name), (
            f"final ordering entry {final_entry!r} does not resolve to the primary key "
            f"('pk' or {pk_name!r}) -- the queryset actually handed to DRF's paginator "
            f"is not totally ordered"
        )
        # And the pre-existing Meta.ordering key keeps its position ahead of it.
        assert order_by[0] == "-created_at"


class TestOffsetShiftKnownLimitation:
    """Point 3: documents a limitation, does not prove the mechanism works.

    A row that sorts BEFORE the page-1/page-2 boundary and is inserted while
    a client is mid-walk pushes every later row down one slot. The next
    OFFSET then re-serves the previous page's last row. ADR-0023 says this
    explicitly is NOT fixed by the total-ordering tiebreaker (it is a
    property of LIMIT/OFFSET pagination itself), so this test's job is to
    keep that fact visible, not to demonstrate success.
    """

    def test_offset_shift_still_produces_a_duplicate(self, db, admin_user):
        commercial_document = StandardCommercialDocumentFactory.create()
        # 5 tied rows, page size 2 -> page 1 has 2 rows, more remain.
        rows = _create_tied_media(5, commercial_document)

        pagination_class = type(
            "_OffsetShiftPagination", (TotalOrderingPageNumberPagination,), {"page_size": 2}
        )
        viewset_class = type(
            "_CommercialDocumentMediaWithPagination",
            (CommercialDocumentMediaViewSet,),
            {"pagination_class": pagination_class},
        )

        factory = APIRequestFactory()

        def _list(page):
            request = factory.get(f"/ordering-totality-test/?page={page}")
            force_authenticate(request, user=admin_user)
            return viewset_class.as_view({"get": "list"})(request)

        page_1 = _list(1)
        assert page_1.status_code == 200
        page_1_ids = [item["id"] for item in page_1.data["results"]]
        assert len(page_1_ids) == 2

        # Insert a row that sorts BEFORE the current page-1/page-2 boundary:
        # ordering is `-created_at` then pk, so a strictly later created_at
        # sorts first.
        newest = CommercialDocumentMedia.objects.create(
            workspace=commercial_document.workspace,
            commercial_document=commercial_document,
            s3_url="https://example-bucket.invalid/media-inserted.pdf",
            s3_key="media-inserted.pdf",
            status="completed",
            media_type="application/pdf",
        )
        CommercialDocumentMedia.objects.filter(pk=newest.pk).update(
            created_at=rows[0].created_at + datetime.timedelta(seconds=10)
        )

        page_2 = _list(2)
        assert page_2.status_code == 200
        page_2_ids = [item["id"] for item in page_2.data["results"]]

        # The inserted row shifted everything down by one slot, so page 2
        # now re-serves whatever page 1 served last: a duplicate across the
        # walk. This is the offset-shift limitation, not a bug in this PR's
        # ordering fix -- it is inherent to LIMIT/OFFSET pagination and is
        # why BaseAPIClient._get_object_list still deduplicates by id.
        assert set(page_1_ids) & set(page_2_ids), (
            "expected the classic offset-shift duplicate (a row inserted ahead of the "
            "page boundary re-served on the next page); if this no longer reproduces, "
            "the walk semantics changed and the surrounding docstring/claims need to be "
            "re-checked, not silently deleted"
        )
