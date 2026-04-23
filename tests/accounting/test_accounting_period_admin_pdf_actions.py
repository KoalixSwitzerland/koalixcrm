# -*- coding: utf-8 -*-
"""Verifies that the AccountingPeriod admin actions queue async PDF
exports (via PDFExportProcess) instead of running FOP in-process.

Asserts the wire contract the Java pdf-export-service relies on:
source_model="AccountingPeriod" and the right template_set FK is
attached so AccountingReportType.resolve(...) on the worker side can
distinguish balance sheet from profit/loss.
"""
import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory

from koalixcrm.accounting.models.accounting_period import (
    AccountingPeriod,
    OptionAccountingPeriod,
)
from koalixcrm.core.models.pdf_export_process import PDFExportProcess
from koalixcrm.core.models.workspace import Workspace
from koalixcrm.djangoUserExtension.models.document_template import DocumentTemplate


@pytest.fixture
def setup(db):
    workspace, _ = Workspace.objects.get_or_create(
        name='Default Workspace', defaults={'is_active': True}
    )
    bs_template = DocumentTemplate.objects.create(
        workspace=workspace, title='BS', xsl_file='xsl/bs.xsl',
    )
    pl_template = DocumentTemplate.objects.create(
        workspace=workspace, title='PL', xsl_file='xsl/pl.xsl',
    )
    period = AccountingPeriod.objects.create(
        title='FY 2018', begin='2018-01-01', end='2018-12-31',
        template_set_balance_sheet=bs_template,
        template_profit_loss_statement=pl_template,
    )
    user = User.objects.create_superuser('admin', 'a@b.c', 'pw')
    admin_obj = OptionAccountingPeriod(AccountingPeriod, AdminSite())
    return {
        'workspace': workspace, 'bs': bs_template, 'pl': pl_template,
        'period': period, 'user': user, 'admin': admin_obj,
    }


def _request(user, workspace):
    """Build a request with the bits the admin action reads:
    user, active_workspace, and a messages backend."""
    req = RequestFactory().get('/')
    req.user = user
    req.active_workspace = workspace
    req.session = {}
    req._messages = FallbackStorage(req)
    return req


@pytest.mark.django_db
class TestAccountingPeriodAsyncPdfActions:

    def test_balance_sheet_action_queues_process_with_balance_template(self, setup):
        req = _request(setup['user'], setup['workspace'])
        before = PDFExportProcess.objects.count()

        setup['admin'].create_pdf_of_balance_sheet(
            req, AccountingPeriod.objects.filter(pk=setup['period'].pk)
        )

        assert PDFExportProcess.objects.count() == before + 1
        proc = PDFExportProcess.objects.latest('id')
        assert proc.source_model == 'AccountingPeriod'
        assert proc.source_id == setup['period'].id
        assert proc.template_set_id == setup['bs'].id
        assert proc.triggered_by_id == setup['user'].id
        assert proc.workspace_id == setup['workspace'].id

    def test_profit_loss_action_queues_process_with_pl_template(self, setup):
        req = _request(setup['user'], setup['workspace'])

        setup['admin'].create_pdf_of_profit_loss_statement(
            req, AccountingPeriod.objects.filter(pk=setup['period'].pk)
        )

        proc = PDFExportProcess.objects.latest('id')
        assert proc.template_set_id == setup['pl'].id

    def test_missing_template_skips_period_and_does_not_queue(self, setup):
        # Period without the balance-sheet template — action should skip it.
        bare = AccountingPeriod.objects.create(
            title='FY 2019', begin='2019-01-01', end='2019-12-31',
            template_set_balance_sheet=None,
            template_profit_loss_statement=setup['pl'],
        )
        req = _request(setup['user'], setup['workspace'])
        before = PDFExportProcess.objects.count()

        setup['admin'].create_pdf_of_balance_sheet(
            req, AccountingPeriod.objects.filter(pk=bare.pk)
        )

        assert PDFExportProcess.objects.count() == before
