# -*- coding: utf-8 -*-
"""
Unit tests for `BaseAPIClient._get_object_list` / `_walk_object_pages`
(the offset-shift detection added alongside ADR-0023 — see the docstring on
`ListWalkIncompleteError` in koalixcrm/shared/api_client.py).

ADR-0023 gives a total ordering, which removes tie nondeterminism. It does
NOT remove offset shift: a row inserted or deleted ahead of the page
boundary while a client walks pages moves every later row by a slot, so a
row can be served twice (dedup catches it) or skipped entirely (nothing
catches it -- silent loss). Comparing the envelope's `count` across pages
detects that the set moved underneath the walk.

`_make_request` is the natural seam: patched here to return a scripted
sequence of page dicts, so no HTTP and no live server is involved.
"""
from __future__ import annotations

from unittest import mock

import pytest

from koalixcrm.shared.api_client import (
    BaseAPIClient,
    ListWalkIncompleteError,
    _RETRY_DELAY_MAX_S,
    _RETRY_DELAY_MIN_S,
)
from koalixcrm.shared.object_cache import ObjectCache


class _FakeDTO:
    """Minimal stand-in for a client-side DTO -- just needs (data, client) and .id."""

    def __init__(self, data, client=None):
        self._data = data
        self.client = client

    @property
    def id(self):
        return self._data.get('id')


def _make_client() -> BaseAPIClient:
    """Build a BaseAPIClient instance without going through __init__.

    __init__ performs OIDC discovery / session login over real sockets, none
    of which is relevant to `_get_object_list`'s pagination-walk logic. The
    only state that logic touches is `_cache`, `agent_application_path`,
    `uses_workspace_id`/`workspace_id`, and `_make_request` (patched per
    test), so those are set directly.
    """
    client = object.__new__(BaseAPIClient)
    client._cache = ObjectCache()
    client.agent_application_path = '/api/v1/things'
    client.uses_workspace_id = False
    client.workspace_id = None
    return client


def _page(results, count, next_url=None):
    return {'results': results, 'count': count, 'next': next_url, 'previous': None}


@pytest.fixture(autouse=True)
def no_real_sleep():
    """Every test patches time.sleep so the retry path stays instant.

    Tests that need to assert on the sleep call get the same mock via the
    `patched_sleep` fixture below (identical object, just also yielded).
    """
    with mock.patch('koalixcrm.shared.api_client.time.sleep') as sleep_mock:
        yield sleep_mock


@pytest.fixture
def patched_sleep(no_real_sleep):
    return no_real_sleep


class TestStableCountAcrossPages:
    def test_all_rows_returned_and_one_request_per_page(self, patched_sleep):
        client = _make_client()
        page_1 = _page([{'id': 1}, {'id': 2}], count=4, next_url='/api/v1/things?page=2')
        page_2 = _page([{'id': 3}, {'id': 4}], count=4, next_url=None)

        with mock.patch.object(client, '_make_request', side_effect=[page_1, page_2]) as m:
            result = client._get_object_list(_FakeDTO, 'things')

        assert [obj.id for obj in result] == [1, 2, 3, 4]
        assert m.call_count == 2, "a spurious retry must fail this test"
        patched_sleep.assert_not_called()


class TestCountChangesOnPageTwo:
    def test_one_restart_then_success(self, patched_sleep):
        client = _make_client()
        # Attempt 1: page 1 count=4, page 2 count=5 -> mismatch, restart.
        attempt_1_page_1 = _page([{'id': 1}, {'id': 2}], count=4, next_url='/api/v1/things?page=2')
        attempt_1_page_2 = _page([{'id': 3}, {'id': 4}, {'id': 5}], count=5, next_url=None)
        # Attempt 2: consistent walk -> correct full list.
        attempt_2_page_1 = _page([{'id': 1}, {'id': 2}], count=5, next_url='/api/v1/things?page=2')
        attempt_2_page_2 = _page([{'id': 3}, {'id': 4}, {'id': 5}], count=5, next_url=None)

        with mock.patch.object(
            client, '_make_request',
            side_effect=[attempt_1_page_1, attempt_1_page_2, attempt_2_page_1, attempt_2_page_2],
        ) as m:
            result = client._get_object_list(_FakeDTO, 'things')

        assert [obj.id for obj in result] == [1, 2, 3, 4, 5]
        assert m.call_count == 4
        patched_sleep.assert_called_once()
        (delay,), _ = patched_sleep.call_args
        assert _RETRY_DELAY_MIN_S <= delay <= _RETRY_DELAY_MAX_S


class TestCountDiffersOnBothAttempts:
    def test_raises_list_walk_incomplete_error(self, patched_sleep):
        client = _make_client()
        attempt_1_page_1 = _page([{'id': 1}], count=3, next_url='/api/v1/things?page=2')
        attempt_1_page_2 = _page([{'id': 2}, {'id': 3}], count=4, next_url=None)
        attempt_2_page_1 = _page([{'id': 1}], count=4, next_url='/api/v1/things?page=2')
        attempt_2_page_2 = _page([{'id': 2}, {'id': 3}, {'id': 4}], count=5, next_url=None)

        with mock.patch.object(
            client, '_make_request',
            side_effect=[attempt_1_page_1, attempt_1_page_2, attempt_2_page_1, attempt_2_page_2],
        ):
            with pytest.raises(ListWalkIncompleteError) as exc_info:
                client._get_object_list(_FakeDTO, 'things')

        message = str(exc_info.value)
        assert 'things' in message
        assert '4' in message  # expected count from attempt 2's first page
        assert '5' in message  # changed count from attempt 2's second page
        patched_sleep.assert_called_once()


class TestBareArrayResponse:
    def test_non_paginated_response_unaffected(self, patched_sleep):
        client = _make_client()
        bare_array = [{'id': 1}, {'id': 2}, {'id': 3}]

        with mock.patch.object(client, '_make_request', side_effect=[bare_array]) as m:
            result = client._get_object_list(_FakeDTO, 'things')

        assert [obj.id for obj in result] == [1, 2, 3]
        assert m.call_count == 1
        patched_sleep.assert_not_called()


class TestMissingOrNonIntCount:
    def test_no_count_key_check_does_not_fire(self, patched_sleep):
        client = _make_client()
        page_1 = {'results': [{'id': 1}], 'next': '/api/v1/things?page=2', 'previous': None}
        page_2 = {'results': [{'id': 2}], 'next': None, 'previous': None}

        with mock.patch.object(client, '_make_request', side_effect=[page_1, page_2]) as m:
            result = client._get_object_list(_FakeDTO, 'things')

        assert [obj.id for obj in result] == [1, 2]
        assert m.call_count == 2
        patched_sleep.assert_not_called()

    def test_non_int_count_check_does_not_fire(self, patched_sleep):
        client = _make_client()
        page_1 = _page([{'id': 1}], count='unknown', next_url='/api/v1/things?page=2')
        page_2 = _page([{'id': 2}], count='unknown', next_url=None)

        with mock.patch.object(client, '_make_request', side_effect=[page_1, page_2]) as m:
            result = client._get_object_list(_FakeDTO, 'things')

        assert [obj.id for obj in result] == [1, 2]
        assert m.call_count == 2
        patched_sleep.assert_not_called()


class TestDedupById:
    def test_duplicate_id_across_pages_kept_once_first_occurrence_wins_order_preserved(self, patched_sleep):
        client = _make_client()
        # id=2 appears on both pages (e.g. offset shift re-serving a row).
        # The payload differs so we can tell which occurrence survived.
        page_1 = _page(
            [{'id': 1, 'marker': 'first'}, {'id': 2, 'marker': 'first'}],
            count=3, next_url='/api/v1/things?page=2',
        )
        page_2 = _page(
            [{'id': 2, 'marker': 'second'}, {'id': 3, 'marker': 'second'}],
            count=3, next_url=None,
        )

        with mock.patch.object(client, '_make_request', side_effect=[page_1, page_2]) as m:
            result = client._get_object_list(_FakeDTO, 'things')

        assert [obj.id for obj in result] == [1, 2, 3]
        obj_2 = next(obj for obj in result if obj.id == 2)
        assert obj_2._data['marker'] == 'first', "first occurrence must win"
        assert m.call_count == 2
        patched_sleep.assert_not_called()
