# -*- coding: utf-8 -*-
from django.contrib import admin

from koalixcrm.contracts.admin.commercial_document_admin import (
    OptionCommercialDocument,  # noqa: F401
)
from koalixcrm.contracts.admin.commercial_document_media_admin import (  # noqa: F401
    CommercialDocumentS3MediaAdmin,
    CommercialDocumentS3MediaInline,
)
from koalixcrm.contracts.admin.commercial_document_position_admin import (
    CommercialDocumentInlinePosition,  # noqa: F401
)
from koalixcrm.contracts.admin.contract_admin import OptionContract  # noqa: F401
from koalixcrm.contracts.admin.credit_note_admin import (  # noqa: F401
    InlineCreditNote,
    OptionCreditNote,
)
from koalixcrm.contracts.admin.despatch_advice_admin import (
    OptionDespatchAdvice,  # noqa: F401
)
from koalixcrm.contracts.admin.invoice_admin import (  # noqa: F401
    InlineInvoice,
    OptionInvoice,
)
from koalixcrm.contracts.admin.payment_reminder_admin import (
    OptionPaymentReminder,  # noqa: F401
)
from koalixcrm.contracts.admin.purchase_order_admin import (
    OptionPurchaseOrder,  # noqa: F401
)
from koalixcrm.contracts.admin.quotation_admin import (  # noqa: F401
    InlineQuotation,
    OptionQuotation,
)
from koalixcrm.contracts.admin.sales_order_admin import OptionSalesOrder  # noqa: F401
from koalixcrm.contracts.models.commercial_document_media import CommercialDocumentS3Media
from koalixcrm.contracts.models.contract import Contract
from koalixcrm.contracts.models.credit_note import CreditNote
from koalixcrm.contracts.models.despatch_advice import DespatchAdvice
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.contracts.models.payment_reminder import PaymentReminder
from koalixcrm.contracts.models.purchase_order import PurchaseOrder
from koalixcrm.contracts.models.quotation import Quotation
from koalixcrm.contracts.models.sales_order import SalesOrder

admin.site.register(CommercialDocumentS3Media, CommercialDocumentS3MediaAdmin)
admin.site.register(Contract, OptionContract)
admin.site.register(Quotation, OptionQuotation)
admin.site.register(SalesOrder, OptionSalesOrder)
admin.site.register(DespatchAdvice, OptionDespatchAdvice)
admin.site.register(Invoice, OptionInvoice)
admin.site.register(PaymentReminder, OptionPaymentReminder)
admin.site.register(PurchaseOrder, OptionPurchaseOrder)
admin.site.register(CreditNote, OptionCreditNote)
