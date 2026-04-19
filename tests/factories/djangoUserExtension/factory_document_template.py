# -*- coding: utf-8 -*-

import factory
from koalixcrm.djangoUserExtension.models import *


class StandardQuotationTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuotationTemplate

    title = "This is a test Quotation Template"
    xsl_file = "~/path/to/xsl_file.xsl"
    fop_config_file = "~/path/to/fop_config_file.xml"
    logo = "~/path/to/logo_file.jpg"


class StandardInvoiceTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InvoiceTemplate

    title = "This is a test Invoice Template"
    xsl_file = "~/path/to/xsl_file.xsl"
    fop_config_file = "~/path/to/fop_config_file.xml"
    logo = "~/path/to/logo_file.jpg"


class StandardDespatchAdviceTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DespatchAdviceTemplate

    title = "This is a test Despatch Advice Template"
    xsl_file = "~/path/to/xsl_file.xsl"
    fop_config_file = "~/path/to/fop_config_file.xml"
    logo = "~/path/to/logo_file.jpg"


class StandardPaymentReminderTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentReminderTemplate

    title = "This is a test Payment Reminder Template"
    xsl_file = "~/path/to/xsl_file.xsl"
    fop_config_file = "~/path/to/fop_config_file.xml"
    logo = "~/path/to/logo_file.jpg"


class StandardPurchaseOrderTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseOrderTemplate

    title = "This is a test Purchase Order Template"
    xsl_file = "~/path/to/xsl_file.xsl"
    fop_config_file = "~/path/to/fop_config_file.xml"
    logo = "~/path/to/logo_file.jpg"


class StandardSalesOrderTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SalesOrderTemplate

    title = "This is a test Sales Order Template"
    xsl_file = "~/path/to/xsl_file.xsl"
    fop_config_file = "~/path/to/fop_config_file.xml"
    logo = "~/path/to/logo_file.jpg"


class StandardBalanceSheetTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BalanceSheetTemplate

    title = "This is a test Balance Sheet Template"
    xsl_file = "~/path/to/xsl_file.xsl"
    fop_config_file = "~/path/to/fop_config_file.xml"
    logo = "~/path/to/logo_file.jpg"


class StandardProfitLossStatementTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProfitLossStatementTemplate

    title = "This is a test Profit Loss Statement Template"
    xsl_file = "~/path/to/xsl_file.xsl"
    fop_config_file = "~/path/to/fop_config_file.xml"
    logo = "~/path/to/logo_file.jpg"


class StandardMonthlyProjectSummaryTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MonthlyProjectSummaryTemplate

    title = "This is a test Purchase Order Template"
    xsl_file = "~/path/to/xsl_file.xsl"
    fop_config_file = "~/path/to/fop_config_file.xml"
    logo = "~/path/to/logo_file.jpg"
