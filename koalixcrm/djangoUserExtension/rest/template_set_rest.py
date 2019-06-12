from rest_framework import serializers

from koalixcrm.djangoUserExtension.user_extension.template_set import TemplateSet
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionInvoiceTemplateJSONSerializer
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionQuoteTemplateJSONSerializer
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionDeliveryNoteTemplateJSONSerializer
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionPaymentReminderTemplateJSONSerializer
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionPurchaseConfirmationTemplateJSONSerializer
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionProfitLossStatementTemplateJSONSerializer
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionPurchaseOrderTemplateJSONSerializer
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionBalanceSheetTemplateJSONSerializer
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer
from koalixcrm.djangoUserExtension.rest.document_template_rest import OptionWorkReportTemplateJSONSerializer
from koalixcrm.djangoUserExtension.user_extension.document_template import InvoiceTemplate
from koalixcrm.djangoUserExtension.user_extension.document_template import QuoteTemplate
from koalixcrm.djangoUserExtension.user_extension.document_template import DeliveryNoteTemplate
from koalixcrm.djangoUserExtension.user_extension.document_template import PaymentReminderTemplate
from koalixcrm.djangoUserExtension.user_extension.document_template import PurchaseOrderTemplate
from koalixcrm.djangoUserExtension.user_extension.document_template import PurchaseConfirmationTemplate
from koalixcrm.djangoUserExtension.user_extension.document_template import ProfitLossStatementTemplate
from koalixcrm.djangoUserExtension.user_extension.document_template import BalanceSheetTemplate
from koalixcrm.djangoUserExtension.user_extension.document_template import MonthlyProjectSummaryTemplate
from koalixcrm.djangoUserExtension.user_extension.document_template import WorkReportTemplate


class OptionTemplateSetJSONSerializer(serializers.HyperlinkedModelSerializer):
    invoiceTemplate = OptionInvoiceTemplateJSONSerializer(source='invoice_template', read_only=True)
    quoteTemplate = OptionQuoteTemplateJSONSerializer(source='quote_template', read_only=True)
    deliveryNoteTemplate = OptionDeliveryNoteTemplateJSONSerializer(source='delivery_note_template', read_only=True)
    paymentReminderTemplate = OptionPaymentReminderTemplateJSONSerializer(source='purchase_confirmation_template', read_only=True)
    purchaseConfirmation_template = OptionPurchaseConfirmationTemplateJSONSerializer(source='user', read_only=True)
    purchaseOrderTemplate = OptionPurchaseOrderTemplateJSONSerializer(source='purchase_order_template', read_only=True)
    profitLossStatementTemplate = OptionProfitLossStatementTemplateJSONSerializer(source='profit_loss_statement_template', read_only=True)
    balanceSheetStatementTemplate = OptionBalanceSheetTemplateJSONSerializer(source='balance_sheet_statement_template', read_only=True)
    monthlyProjectSummaryTemplate = OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer(source='monthly_project_summary_template', read_only=True)
    workReportTemplate = OptionWorkReportTemplateJSONSerializer(source='work_report_template', read_only=True)

    class Meta:
        model = TemplateSet
        fields = ('title',
                  'invoiceTemplate',
                  'quoteTemplate',
                  'deliveryNoteTemplate',
                  'paymentReminderTemplate',
                  'purchaseConfirmation_template',
                  'purchaseOrderTemplate',
                  'profitLossStatementTemplate',
                  'balanceSheetStatementTemplate',
                  'monthlyProjectSummaryTemplate',
                  'workReportTemplate')


class TemplateSetJSONSerializer(serializers.HyperlinkedModelSerializer):
    invoiceTemplate = OptionInvoiceTemplateJSONSerializer(source='invoice_template')
    quoteTemplate = OptionQuoteTemplateJSONSerializer(source='quote_template')
    deliveryNoteTemplate = OptionDeliveryNoteTemplateJSONSerializer(source='delivery_note_template')
    paymentReminderTemplate = OptionPaymentReminderTemplateJSONSerializer(source='purchase_confirmation_template')
    purchaseOrderTemplate = OptionPurchaseConfirmationTemplateJSONSerializer(source='user')
    purchaseOrderTemplate = OptionPurchaseOrderTemplateJSONSerializer(source='purchase_order_template')
    profitLossStatementTemplate = OptionProfitLossStatementTemplateJSONSerializer(source='profit_loss_statement_template')
    balanceSheetStatementTemplate = OptionBalanceSheetTemplateJSONSerializer(source='balance_sheet_statement_template')
    monthlyProjectSummaryTemplate = OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer(source='monthly_project_summary_template')
    workReportTemplate = OptionWorkReportTemplateJSONSerializer(source='work_report_template')

    class Meta:
        model = TemplateSet
        fields = ('title',
                  'invoiceTemplate',
                  'quoteTemplate',
                  'deliveryNoteTemplate',
                  'paymentReminderTemplate',
                  'purchaseConfirmation_template',
                  'purchaseOrderTemplate',
                  'profitLossStatementTemplate',
                  'balanceSheetStatementTemplate',
                  'monthlyProjectSummaryTemplate',
                  'workReportTemplate')

    def create(self, validated_data):
        template_set = TemplateSet()
        # Deserialize invoice template
        invoice_template = validated_data.pop('invoiceTemplate')
        if invoice_template:
            if invoice_template.get('id', None):
                template_set.invoice_template = InvoiceTemplate.objects.get(id=invoice_template.get('id', None))
            else:
                template_set.invoice_template = None
        # Deserialize quote template
        quote_template = validated_data.pop('quoteTemplate')
        if quote_template:
            if quote_template.get('id', None):
                template_set.quote_template = QuoteTemplate.objects.get(id=quote_template.get('id', None))
            else:
                template_set.quote_template = None
        # Deserialize delivery note template
        delivery_note_template = validated_data.pop('deliveryNoteTemplate')
        if delivery_note_template:
            if delivery_note_template.get('id', None):
                template_set.delivery_note_template = DeliveryNoteTemplate.objects.get(id=delivery_note_template.get('id', None))
            else:
                template_set.delivery_note_template = None
        # Deserialize payment reminder template
        payment_reminder_template = validated_data.pop('paymentReminderTemplate')
        if payment_reminder_template:
            if payment_reminder_template.get('id', None):
                template_set.payment_reminder_template = PaymentReminderTemplate.objects.get(id=payment_reminder_template.get('id', None))
            else:
                template_set.payment_reminder_template = None
        # Deserialize purchase_confirmation_template
        purchase_confirmation_template = validated_data.pop('purchaseConfirmationTemplate')
        if purchase_confirmation_template:
            if purchase_confirmation_template.get('id', None):
                template_set.purchase_confirmation_template = PurchaseConfirmationTemplate.objects.get(id=purchase_confirmation_template.get('id', None))
            else:
                template_set.purchase_confirmation_template = None
        # Deserialize purchase_order_template
        purchase_order_template = validated_data.pop('purchaseOrderTemplate')
        if purchase_order_template:
            if purchase_order_template.get('id', None):
                template_set.purchase_order_template = PurchaseOrderTemplate.objects.get(id=purchase_order_template.get('id', None))
            else:
                template_set.purchase_order_template = None
        # Deserialize purchase_confirmation_template
        purchase_confirmation_template = validated_data.pop('purchaseConfirmationTemplate')
        if purchase_confirmation_template:
            if purchase_confirmation_template.get('id', None):
                template_set.purchase_confirmation_template = PurchaseConfirmationTemplate.objects.get(id=purchase_confirmation_template.get('id', None))
            else:
                template_set.purchase_confirmation_template = None
        # Deserialize profit_loss_statement_template
        profit_loss_statement_template = validated_data.pop('profitLossStatementTemplate')
        if profit_loss_statement_template:
            if profit_loss_statement_template.get('id', None):
                template_set.profit_loss_statement_template = ProfitLossStatementTemplate.objects.get(id=profit_loss_statement_template.get('id', None))
            else:
                template_set.profit_loss_statement_template = None
        # Deserialize balance_sheet_statement_template
        balance_sheet_statement_template = validated_data.pop('balanceSheetStatementTemplate')
        if balance_sheet_statement_template:
            if balance_sheet_statement_template.get('id', None):
                template_set.balance_sheet_statement_template = BalanceSheetTemplate.objects.get(id=balance_sheet_statement_template.get('id', None))
            else:
                template_set.balance_sheet_statement_template = None
        # Deserialize monthly_project_summary_template
        monthly_project_summary_template = validated_data.pop('monthlyProjectSummaryTemplate')
        if monthly_project_summary_template:
            if monthly_project_summary_template.get('id', None):
                template_set.monthly_project_summary_template = MonthlyProjectSummaryTemplate.objects.get(id=monthly_project_summary_template.get('id', None))
            else:
                template_set.monthly_project_summary_template = None
        # Deserialize work_report_template
        work_report_template = validated_data.pop('workReportTemplate')
        if work_report_template:
            if work_report_template.get('id', None):
                template_set.work_report_template = WorkReportTemplate.objects.get(id=work_report_template.get('id', None))
            else:
                template_set.work_report_template = None
        template_set.save()

    def update(self, template_set, validated_data):
        # Deserialize invoice template
        invoice_template = validated_data.pop('invoiceTemplate')
        if invoice_template:
            if invoice_template.get('id', None):
                template_set.invoice_template = InvoiceTemplate.objects.get(id=invoice_template.get('id', None))
            else:
                template_set.invoice_template = template_set.invoice_template_id
        else:
            template_set.invoice_template = None
        # Deserialize quote template
        quote_template = validated_data.pop('quoteTemplate')
        if quote_template:
            if quote_template.get('id', None):
                template_set.quote_template = QuoteTemplate.objects.get(id=quote_template.get('id', None))
            else:
                template_set.quote_template = template_set.quote_template_id
        else:
            template_set.quote_template = None
        # Deserialize delivery note template
        delivery_note_template = validated_data.pop('deliveryNoteTemplate')
        if delivery_note_template:
            if delivery_note_template.get('id', None):
                template_set.delivery_note_template = DeliveryNoteTemplate.objects.get(id=delivery_note_template.get('id', None))
            else:
                template_set.delivery_note_template = template_set.delivery_note_template_id
        else:
            template_set.delivery_note_template = None
        # Deserialize payment reminder template
        payment_reminder_template = validated_data.pop('paymentReminderTemplate')
        if payment_reminder_template:
            if payment_reminder_template.get('id', None):
                template_set.payment_reminder_template = PaymentReminderTemplate.objects.get(id=payment_reminder_template.get('id', None))
            else:
                template_set.payment_reminder_template = template_set.payment_reminder_template_id
        else:
            template_set.payment_reminder_template = None
        # Deserialize purchase_confirmation_template
        purchase_confirmation_template = validated_data.pop('purchaseConfirmationTemplate')
        if purchase_confirmation_template:
            if purchase_confirmation_template.get('id', None):
                template_set.purchase_confirmation_template = PurchaseConfirmationTemplate.objects.get(id=purchase_confirmation_template.get('id', None))
            else:
                template_set.purchase_confirmation_template = template_set.purchase_confirmation_template_id
        else:
            template_set.purchase_confirmation_template = None
        # Deserialize purchase_order_template
        purchase_order_template = validated_data.pop('purchaseOrderTemplate')
        if purchase_order_template:
            if purchase_order_template.get('id', None):
                template_set.purchase_order_template = PurchaseOrderTemplate.objects.get(id=purchase_order_template.get('id', None))
            else:
                template_set.purchase_order_template = template_set.purchase_order_template_id
        else:
            template_set.work_report_template = None
        # Deserialize purchase_confirmation_template
        purchase_confirmation_template = validated_data.pop('purchaseConfirmationTemplate')
        if purchase_confirmation_template:
            if purchase_confirmation_template.get('id', None):
                template_set.purchase_confirmation_template = PurchaseConfirmationTemplate.objects.get(id=purchase_confirmation_template.get('id', None))
            else:
                template_set.purchase_confirmation_template = template_set.purchase_confirmation_template_id
        else:
            template_set.purchase_confirmation_template = None
        # Deserialize profit_loss_statement_template
        profit_loss_statement_template = validated_data.pop('profitLossStatementTemplate')
        if profit_loss_statement_template:
            if profit_loss_statement_template.get('id', None):
                template_set.profit_loss_statement_template = ProfitLossStatementTemplate.objects.get(id=profit_loss_statement_template.get('id', None))
            else:
                template_set.profit_loss_statement_template = template_set.profit_loss_statement_template_id
        else:
            template_set.profit_loss_statement_template = None
        # Deserialize balance_sheet_statement_template
        balance_sheet_statement_template = validated_data.pop('balanceSheetStatementTemplate')
        if balance_sheet_statement_template:
            if balance_sheet_statement_template.get('id', None):
                template_set.balance_sheet_statement_template = BalanceSheetTemplate.objects.get(id=balance_sheet_statement_template.get('id', None))
            else:
                template_set.balance_sheet_statement_template = template_set.balance_sheet_statement_template_id
        else:
            template_set.balance_sheet_statement_template = None
        # Deserialize monthly_project_summary_template
        monthly_project_summary_template = validated_data.pop('monthlyProjectSummaryTemplate')
        if monthly_project_summary_template:
            if monthly_project_summary_template.get('id', None):
                template_set.monthly_project_summary_template = MonthlyProjectSummaryTemplate.objects.get(id=monthly_project_summary_template.get('id', None))
            else:
                template_set.monthly_project_summary_template = template_set.monthly_project_summary_template_id
        else:
            template_set.monthly_project_summary_template = None
        # Deserialize work_report_template
        work_report_template = validated_data.pop('workReportTemplate')
        if work_report_template:
            if work_report_template.get('id', None):
                template_set.work_report_template = WorkReportTemplate.objects.get(id=work_report_template.get('id', None))
            else:
                template_set.work_report_template = template_set.work_report_template_id
        else:
            template_set.work_report_template = None
        template_set.save()
