# -*- coding: utf-8 -*-

import factory
from koalixcrm.djangoUserExtension.models import *
from filebrowser.base import FileObject


class StandardQuoteTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuoteTemplate

    title = "This is a test Quote Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")


class StandardInvoiceTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InvoiceTemplate

    title = "This is a test Invoice Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")


class StandardDeliveryNoteTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeliveryNoteTemplate

    title = "This is a test Delivery Note Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")


class StandardPaymentReminderTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentReminderTemplate

    title = "This is a test Payment Reminder Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")


class StandardPurchaseOrderTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseOrderTemplate

    title = "This is a test Purchase Order Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")


class StandardPurchaseConfirmationTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseConfirmationTemplate

    title = "This is a test Purchase Confirmation Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")


class StandardBalanceSheetTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BalanceSheetTemplate

    title = "This is a test Balance Sheet Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")


class StandardProfitLossStatementTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProfitLossStatementTemplate

    title = "This is a test Profit Loss Statement Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")


class StandardMonthlyProjectSummaryTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MonthlyProjectSummaryTemplate

    title = "This is a test Purchase Order Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")
