# -*- coding: utf-8 -*-
"""
Unit tests for the REST endpoints added in stage 1 of the PDF-service migration.

These endpoints are consumed by the Java PDF worker. The tests exercise the
Django side only — they mock out presigned-URL generation so no real S3 is
required.
"""
from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from koalixcrm.core.models.pdf_export_process import PDFExportProcess


@pytest.fixture
def api_client(admin_user):
    client = APIClient()
    client.force_authenticate(admin_user)
    return client


@pytest.fixture
def pdf_export_process(db):
    from koalixcrm.core.models.workspace import Workspace
    ws, _ = Workspace.objects.get_or_create(name='Default Workspace', defaults={'is_active': True})
    return PDFExportProcess.objects.create(
        source_model="Invoice",
        source_id=1,
        status="pending",
        workspace=ws,
    )


@pytest.mark.django_db
class TestPDFExportProcessEndpoint:
    # NOTE: A plain GET-after-create test for this endpoint belongs in the
    # integration suite, not here. Creating a PDFExportProcess fires
    # `trigger_pdf_export`, which publishes to SQS and flips the row to
    # `failed` when SQS is unreachable — which is always the case in the
    # unit-django profile (no ElasticMQ). The remaining tests in this class
    # assert invariants that hold regardless of that signal's outcome.

    def test_patch_status_transitions_to_completed(self, api_client, pdf_export_process):
        resp = api_client.patch(
            f"/koalixcrm_core/api/v1/1/pdf-export-processes/{pdf_export_process.id}/",
            {"status": "completed", "result_url": "http://example.test/pdf.pdf"},
            format="json",
        )
        assert resp.status_code == 200
        pdf_export_process.refresh_from_db()
        assert pdf_export_process.status == "completed"
        assert pdf_export_process.result_url == "http://example.test/pdf.pdf"

    def test_source_fields_are_read_only(self, api_client, pdf_export_process):
        resp = api_client.patch(
            f"/koalixcrm_core/api/v1/1/pdf-export-processes/{pdf_export_process.id}/",
            {"source_model": "Quotation", "source_id": 999},
            format="json",
        )
        assert resp.status_code == 200
        pdf_export_process.refresh_from_db()
        assert pdf_export_process.source_model == "Invoice"
        assert pdf_export_process.source_id == 1

    def test_create_is_not_allowed(self, api_client):
        resp = api_client.post(
            "/koalixcrm_core/api/v1/1/pdf-export-processes/",
            {"source_model": "Invoice", "source_id": 1, "status": "pending"},
            format="json",
        )
        assert resp.status_code == 405

    def test_delete_is_not_allowed(self, api_client, pdf_export_process):
        resp = api_client.delete(f"/koalixcrm_core/api/v1/1/pdf-export-processes/{pdf_export_process.id}/")
        assert resp.status_code == 405


@pytest.mark.django_db
class TestDocumentTemplateEndpoint:
    @pytest.fixture
    def document_template(self, db):
        from koalixcrm.djangoUserExtension.tests.factories.document_template_factory import (
            StandardQuotationTemplateFactory,
        )

        return StandardQuotationTemplateFactory()

    def test_retrieve_returns_sub_resource_hrefs(self, api_client, document_template):
        resp = api_client.get(f"/koalixcrm_core/api/v1/1/document-templates/{document_template.id}/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == document_template.id
        assert data["xsl_href"].endswith(f"/koalixcrm_core/api/v1/1/document-templates/{document_template.id}/xsl/")
        assert data["fop_config_href"].endswith(
            f"/koalixcrm_core/api/v1/1/document-templates/{document_template.id}/fop-config/"
        )
        assert data["logo_href"].endswith(
            f"/koalixcrm_core/api/v1/1/document-templates/{document_template.id}/logo/"
        )

    def test_xsl_detail_action_redirects_to_presigned_url(
        self, api_client, document_template
    ):
        if not document_template.xsl_file:
            pytest.skip("factory did not attach an xsl_file")
        with patch(
            "koalixcrm.djangoUserExtension.views.document_template_view_set.presigned_get_url_for_field",
            return_value="https://example.test/presigned-xsl",
        ):
            resp = api_client.get(
                f"/koalixcrm_core/api/v1/1/document-templates/{document_template.id}/xsl/", follow=False
            )
        assert resp.status_code == 302
        assert resp["Location"] == "https://example.test/presigned-xsl"

    def test_missing_optional_asset_returns_404(self, api_client, document_template):
        document_template.logo = None
        document_template.save()
        resp = api_client.get(f"/koalixcrm_core/api/v1/1/document-templates/{document_template.id}/logo/")
        assert resp.status_code == 404


@pytest.mark.django_db
class TestCommercialDocumentMediaEndpoint:
    def test_post_creates_row(self, api_client):
        from koalixcrm.contracts.tests.factories.invoice_factory import StandardInvoiceFactory

        invoice = StandardInvoiceFactory()
        resp = api_client.post(
            "/koalixcrm_contracts/api/v1/1/commercial-document-media/",
            {
                "commercial_document": invoice.id,
                "s3_url": "pdf-exports/Invoice_1_42.pdf",
                "status": "completed",
                "media_type": "application/pdf",
            },
            format="json",
        )
        assert resp.status_code == 201, resp.content
        body = resp.json()
        assert body["s3_url"] == "pdf-exports/Invoice_1_42.pdf"
        assert body["status"] == "completed"

    def test_post_rejects_absolute_s3_url(self, api_client):
        """WFS ADR-7: the DB stores a relative key, never an absolute URI.

        An absolute URL bakes the endpoint host into the row, which is exactly
        what made the worker's write-back unusable from a browser.
        """
        from koalixcrm.contracts.tests.factories.invoice_factory import StandardInvoiceFactory

        invoice = StandardInvoiceFactory()
        for absolute in (
            "http://minio:9000/koalixcrm-pdf-exports/pdf-exports/Invoice_1_42.pdf",
            "s3://koalixcrm-pdf-exports/pdf-exports/Invoice_1_42.pdf",
            "https://bucket.s3.amazonaws.com/key.pdf",
        ):
            resp = api_client.post(
                "/koalixcrm_contracts/api/v1/1/commercial-document-media/",
                {
                    "commercial_document": invoice.id,
                    "s3_url": absolute,
                    "status": "completed",
                    "media_type": "application/pdf",
                },
                format="json",
            )
            assert resp.status_code == 400, f"{absolute} should be rejected, got {resp.content}"
            assert "s3_url" in resp.json()
