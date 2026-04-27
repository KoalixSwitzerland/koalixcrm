# -*- coding: utf-8 -*-
from django.contrib import admin

from koalixcrm.djangoUserExtension.models import (
    MonthlyProjectSummaryTemplate,
    SalesOrderTemplate,
    WorkReportTemplate,
)
from koalixcrm.djangoUserExtension.models.document_template import (
    BalanceSheetTemplate,
    DespatchAdviceTemplate,
    InvoiceTemplate,
    OptionDocumentTemplate,
    PaymentReminderTemplate,
    ProfitLossStatementTemplate,
    PurchaseOrderTemplate,
    QuotationTemplate,
)

admin.site.register(InvoiceTemplate, OptionDocumentTemplate)
admin.site.register(QuotationTemplate, OptionDocumentTemplate)
admin.site.register(DespatchAdviceTemplate, OptionDocumentTemplate)
admin.site.register(PaymentReminderTemplate, OptionDocumentTemplate)
admin.site.register(PurchaseOrderTemplate, OptionDocumentTemplate)
admin.site.register(SalesOrderTemplate, OptionDocumentTemplate)
admin.site.register(ProfitLossStatementTemplate, OptionDocumentTemplate)
admin.site.register(BalanceSheetTemplate, OptionDocumentTemplate)
admin.site.register(MonthlyProjectSummaryTemplate, OptionDocumentTemplate)
admin.site.register(WorkReportTemplate, OptionDocumentTemplate)
