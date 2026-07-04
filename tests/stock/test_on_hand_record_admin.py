# -*- coding: utf-8 -*-
"""ADR-0011: `OnHandRecord` is a stored projection whose only authorized
write path is `services/movement_posting.py`. Regression test for the QA
finding that `OnHandRecordAdmin` used to allow add/change/delete directly
through Django admin, silently bypassing the movement log (unlike its
sibling `StockBalanceAdmin`, which was already locked down)."""
import pytest
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from koalixcrm.stock.admin.on_hand_record_admin import OnHandRecordAdmin
from koalixcrm.stock.models.on_hand_record import OnHandRecord
from tests.factories.stock.on_hand_record_factory import StandardOnHandRecordFactory


class OnHandRecordAdminReadOnlyTest(TestCase):
    def setUp(self):
        self.admin = OnHandRecordAdmin(OnHandRecord, AdminSite())

    @pytest.mark.back_end_tests
    def test_add_permission_denied(self):
        self.assertFalse(self.admin.has_add_permission(request=None))

    @pytest.mark.back_end_tests
    def test_change_permission_denied(self):
        record = StandardOnHandRecordFactory()
        self.assertFalse(self.admin.has_change_permission(request=None, obj=record))
        self.assertFalse(self.admin.has_change_permission(request=None, obj=None))

    @pytest.mark.back_end_tests
    def test_delete_permission_denied(self):
        record = StandardOnHandRecordFactory()
        self.assertFalse(self.admin.has_delete_permission(request=None, obj=record))

    @pytest.mark.back_end_tests
    def test_all_fields_are_readonly(self):
        field_names = {f.name for f in OnHandRecord._meta.fields}
        self.assertEqual(set(self.admin.readonly_fields), field_names)
