# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.djangoUserExtension.models import (
    PurchaseConfirmationTemplate,
    MonthlyProjectSummaryTemplate,
    WorkReportTemplate,
)
from koalixcrm.djangoUserExtension.user_extension.document_template import (
    InvoiceTemplate,
    QuoteTemplate,
    DeliveryNoteTemplate,
    PaymentReminderTemplate,
    PurchaseOrderTemplate,
    ProfitLossStatementTemplate,
    BalanceSheetTemplate,
    OptionDocumentTemplate,
)

admin.site.register(InvoiceTemplate, OptionDocumentTemplate)
admin.site.register(QuoteTemplate, OptionDocumentTemplate)
admin.site.register(DeliveryNoteTemplate, OptionDocumentTemplate)
admin.site.register(PaymentReminderTemplate, OptionDocumentTemplate)
admin.site.register(PurchaseOrderTemplate, OptionDocumentTemplate)
admin.site.register(PurchaseConfirmationTemplate, OptionDocumentTemplate)
admin.site.register(ProfitLossStatementTemplate, OptionDocumentTemplate)
admin.site.register(BalanceSheetTemplate, OptionDocumentTemplate)
admin.site.register(MonthlyProjectSummaryTemplate, OptionDocumentTemplate)
admin.site.register(WorkReportTemplate, OptionDocumentTemplate)
