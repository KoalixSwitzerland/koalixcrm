# -*- coding: utf-8 -*-
"""koalixcrm#444 -- commercial document admin links must HTML-escape the description."""
import pytest

from koalixcrm.contracts.tests.factories.credit_note_factory import StandardCreditNoteFactory
from koalixcrm.contracts.tests.factories.invoice_factory import StandardInvoiceFactory
from koalixcrm.contracts.tests.factories.quotation_factory import StandardQuotationFactory

PAYLOAD = '<script>alert(1)</script>'  # 25 chars, survives limit_string_length(.., 30)
ESCAPED = '&lt;script&gt;alert(1)&lt;/script&gt;'

CASES = [
    (StandardInvoiceFactory, 'link_to_invoice', 'invoice'),
    (StandardQuotationFactory, 'link_to_quotation', 'quotation'),
    (StandardCreditNoteFactory, 'link_to_credit_note', 'creditnote'),
]
IDS = [c[2] for c in CASES]


@pytest.mark.django_db
@pytest.mark.parametrize('factory_class,method,slug', CASES, ids=IDS)
def test_description_is_escaped(factory_class, method, slug):
    doc = factory_class.create(description=PAYLOAD)
    html = str(getattr(doc, method)())
    assert '<script>' not in html
    assert ESCAPED in html


@pytest.mark.django_db
@pytest.mark.parametrize('factory_class,method,slug', CASES, ids=IDS)
def test_link_unchanged_for_plain_description(factory_class, method, slug):
    doc = factory_class.create(description='Plain description')
    assert str(getattr(doc, method)()) == (
        "<a href='/admin/contract_object_management/%s/%s' >Plain description</a>" % (slug, doc.id)
    )


@pytest.mark.django_db
@pytest.mark.parametrize('factory_class,method,slug', CASES, ids=IDS)
def test_quote_in_description_cannot_break_out(factory_class, method, slug):
    doc = factory_class.create(description='"><img src=x onerror=a>')
    html = str(getattr(doc, method)())
    assert '<img' not in html
