# -*- coding: utf-8 -*-
"""
Reusable regression test for ADR-0023 (Pagination Requires a Total Ordering).

`OrderingTotalityTestCaseMixin` drives any ViewSet's `list` action through
`TotalOrderingPageNumberPagination` (pagination stays disabled project-wide —
see ADR-0023 — so this mixin binds the pagination class itself, it never
flips on `DEFAULT_PAGINATION_CLASS`) and asserts the three properties the ADR
promises:

- a full page walk across a tie group larger than the page size returns
  every row exactly once, no duplicates, no gaps;
- two consecutive identical requests for the same page return the same
  order;
- the response envelope has the standard `count`/`next`/`previous`/`results`
  shape.

Usage — subclass and set:

    viewset_class          the DRF ViewSet under test (as used in urls.py)
    pagination_page_size   a page size small enough to force >1 page for the
                            tie group (default: 3)
    tie_group_size         number of tied rows to create; must exceed
                            pagination_page_size so the walk spans pages
                            (default: 7)

and implement:

    create_tied_rows(count) -> list
        Create exactly `count` persisted rows that compare EQUAL under the
        ViewSet's effective ordering (i.e. a genuine tie group, not merely
        `count` arbitrary rows). Returns the created objects.

Requests are dispatched with `rest_framework.test.APIRequestFactory` directly
against `viewset_class.as_view({'get': 'list'})`, bypassing the URLconf/router
entirely — the mixin does not need `urls.py` to be wired up, and it does not
need to know about workspace-scoped URL kwargs for ViewSets that don't use
them. Authentication uses `force_authenticate` with the `admin_user` fixture
from the project's root conftest.py (a superuser, so `DjangoModelPermissions`
checks pass regardless of the model's app_label/model_name).
"""
from __future__ import annotations

import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from koalixcrm.shared.pagination import TotalOrderingPageNumberPagination

pytestmark = pytest.mark.django_db


class OrderingTotalityTestCaseMixin:
    viewset_class = None
    pagination_page_size = 3
    tie_group_size = 7

    # ------------------------------------------------------------------
    # Hooks subclasses must/can override
    # ------------------------------------------------------------------

    @staticmethod
    def create_tied_rows(count):
        raise NotImplementedError(
            "Subclasses of OrderingTotalityTestCaseMixin must implement "
            "create_tied_rows(count), returning `count` persisted rows that "
            "compare equal under the ViewSet's effective ordering."
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _paginated_viewset_class(self):
        """A throwaway ViewSet subclass with pagination_class bound.

        Pagination stays off project-wide (ADR-0023): no ViewSet in the
        codebase sets `pagination_class`, and no `DEFAULT_PAGINATION_CLASS`
        is registered. This subclass exists only for the duration of the
        test and does not touch the real ViewSet or global settings.
        """
        pagination_class = type(
            "_TestPagination",
            (TotalOrderingPageNumberPagination,),
            {"page_size": self.pagination_page_size},
        )
        return type(
            f"_{self.viewset_class.__name__}WithPagination",
            (self.viewset_class,),
            {"pagination_class": pagination_class},
        )

    def _list(self, admin_user, page=None):
        factory = APIRequestFactory()
        path = "/ordering-totality-test/" if page is None else f"/ordering-totality-test/?page={page}"
        request = factory.get(path)
        force_authenticate(request, user=admin_user)
        view = self._paginated_viewset_class().as_view({"get": "list"})
        return view(request)

    # ------------------------------------------------------------------
    # Tests
    # ------------------------------------------------------------------

    def test_full_page_walk_returns_every_row_exactly_once(self, admin_user):
        assert self.tie_group_size > self.pagination_page_size, (
            "tie_group_size must exceed pagination_page_size so the walk "
            "actually spans multiple pages"
        )
        rows = self.create_tied_rows(self.tie_group_size)
        expected_ids = {row.pk for row in rows}
        assert len(expected_ids) == self.tie_group_size, "create_tied_rows must return distinct rows"

        seen_ids: list[int] = []
        page = 1
        while True:
            response = self._list(admin_user, page=page)
            assert response.status_code == 200, getattr(response, "data", None)
            results = response.data["results"]
            seen_ids.extend(item["id"] for item in results)
            if response.data["next"] is None:
                break
            page += 1
            assert page < 10_000, "pagination walk did not terminate"

        relevant_seen = [pk for pk in seen_ids if pk in expected_ids]
        assert len(relevant_seen) == len(expected_ids), (
            f"expected {len(expected_ids)} tied rows across the walk, saw "
            f"{len(relevant_seen)}: {relevant_seen} (expected ids: {sorted(expected_ids)})"
        )
        assert len(set(relevant_seen)) == len(relevant_seen), f"duplicate row(s) across pages: {relevant_seen}"
        assert set(relevant_seen) == expected_ids

    def test_stable_order_across_repeated_identical_requests(self, admin_user):
        self.create_tied_rows(self.tie_group_size)
        response_1 = self._list(admin_user, page=1)
        response_2 = self._list(admin_user, page=1)
        assert response_1.status_code == 200
        assert response_2.status_code == 200
        ids_1 = [item["id"] for item in response_1.data["results"]]
        ids_2 = [item["id"] for item in response_2.data["results"]]
        assert ids_1 == ids_2

    def test_response_envelope_shape(self, admin_user):
        self.create_tied_rows(self.tie_group_size)
        response = self._list(admin_user, page=1)
        assert response.status_code == 200
        assert set(response.data.keys()) == {"count", "next", "previous", "results"}
        assert isinstance(response.data["results"], list)
        assert response.data["count"] >= self.tie_group_size
