from rest_framework import serializers

from koalixcrm.djangoUserExtension.models.template_set import TemplateSet
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionInvoiceTemplateJSONSerializer
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionQuoteTemplateJSONSerializer
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionDeliveryNoteTemplateJSONSerializer
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionPaymentReminderTemplateJSONSerializer
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionPurchaseConfirmationTemplateJSONSerializer
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionProfitLossStatementTemplateJSONSerializer
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionPurchaseOrderTemplateJSONSerializer
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionBalanceSheetTemplateJSONSerializer
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer
from koalixcrm.djangoUserExtension.serializers.document_template_rest import OptionWorkReportTemplateJSONSerializer
from koalixcrm.djangoUserExtension.models.document_template import InvoiceTemplate
from koalixcrm.djangoUserExtension.models.document_template import QuoteTemplate
from koalixcrm.djangoUserExtension.models.document_template import DeliveryNoteTemplate
from koalixcrm.djangoUserExtension.models.document_template import PaymentReminderTemplate
from koalixcrm.djangoUserExtension.models.document_template import PurchaseOrderTemplate
from koalixcrm.djangoUserExtension.models.document_template import PurchaseConfirmationTemplate
from koalixcrm.djangoUserExtension.models.document_template import ProfitLossStatementTemplate
from koalixcrm.djangoUserExtension.models.document_template import BalanceSheetTemplate
from koalixcrm.djangoUserExtension.models.document_template import MonthlyProjectSummaryTemplate
from koalixcrm.djangoUserExtension.models.document_template import WorkReportTemplate


class OptionTemplateSetJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    invoice_template = OptionInvoiceTemplateJSONSerializer(read_only=True)
    quote_template = OptionQuoteTemplateJSONSerializer(read_only=True)
    delivery_note_template = OptionDeliveryNoteTemplateJSONSerializer(read_only=True)
    payment_reminder_template = OptionPaymentReminderTemplateJSONSerializer(read_only=True)
    purchase_confirmation_template = OptionPurchaseConfirmationTemplateJSONSerializer(read_only=True)
    purchase_order_template = OptionPurchaseOrderTemplateJSONSerializer(read_only=True)
    profit_loss_statement_template = OptionProfitLossStatementTemplateJSONSerializer(read_only=True)
    balance_sheet_statement_template = OptionBalanceSheetTemplateJSONSerializer(read_only=True)
    monthly_project_summary_template = OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer(read_only=True)
    work_report_template = OptionWorkReportTemplateJSONSerializer(read_only=True)

    class Meta:
        model = TemplateSet
        fields = ('id',
                  'title',
                  'invoice_template',
                  'quote_template',
                  'delivery_note_template',
                  'payment_reminder_template',
                  'purchase_confirmation_template',
                  'purchase_order_template',
                  'profit_loss_statement_template',
                  'balance_sheet_statement_template',
                  'monthly_project_summary_template',
                  'work_report_template')


class TemplateSetJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    invoice_template = OptionInvoiceTemplateJSONSerializer(required=False, allow_null=True)
    quote_template = OptionQuoteTemplateJSONSerializer(required=False, allow_null=True)
    delivery_note_template = OptionDeliveryNoteTemplateJSONSerializer(required=False, allow_null=True)
    payment_reminder_template = OptionPaymentReminderTemplateJSONSerializer(required=False, allow_null=True)
    purchase_confirmation_template = OptionPurchaseConfirmationTemplateJSONSerializer(required=False, allow_null=True)
    purchase_order_template = OptionPurchaseOrderTemplateJSONSerializer(required=False, allow_null=True)
    profit_loss_statement_template = OptionProfitLossStatementTemplateJSONSerializer(required=False, allow_null=True)
    balance_sheet_statement_template = OptionBalanceSheetTemplateJSONSerializer(required=False, allow_null=True)
    monthly_project_summary_template = OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer(required=False, allow_null=True)
    work_report_template = OptionWorkReportTemplateJSONSerializer(required=False, allow_null=True)

    class Meta:
        model = TemplateSet
        fields = ('id',
                  'title',
                  'invoice_template',
                  'quote_template',
                  'delivery_note_template',
                  'payment_reminder_template',
                  'purchase_confirmation_template',
                  'purchase_order_template',
                  'profit_loss_statement_template',
                  'balance_sheet_statement_template',
                  'monthly_project_summary_template',
                  'work_report_template')

    def create(self, validated_data):
        template_set = TemplateSet()
        # Deserialize invoice template
        invoice_template = validated_data.pop('invoice_template')
        if invoice_template:
            if invoice_template.get('id', None):
                template_set.invoice_template = InvoiceTemplate.objects.get(id=invoice_template.get('id', None))
            else:
                template_set.invoice_template = None
        # Deserialize quote template
        quote_template = validated_data.pop('quote_template')
        if quote_template:
            if quote_template.get('id', None):
                template_set.quote_template = QuoteTemplate.objects.get(id=quote_template.get('id', None))
            else:
                template_set.quote_template = None
        # Deserialize delivery note template
        delivery_note_template = validated_data.pop('delivery_note_template')
        if delivery_note_template:
            if delivery_note_template.get('id', None):
                template_set.delivery_note_template = DeliveryNoteTemplate.objects.get(id=delivery_note_template.get('id', None))
            else:
                template_set.delivery_note_template = None
        # Deserialize payment reminder template
        payment_reminder_template = validated_data.pop('payment_reminder_template')
        if payment_reminder_template:
            if payment_reminder_template.get('id', None):
                template_set.payment_reminder_template = PaymentReminderTemplate.objects.get(id=payment_reminder_template.get('id', None))
            else:
                template_set.payment_reminder_template = None
        # Deserialize purchase_confirmation_template
        purchase_confirmation_template = validated_data.pop('purchase_confirmation_template')
        if purchase_confirmation_template:
            if purchase_confirmation_template.get('id', None):
                template_set.purchase_confirmation_template = PurchaseConfirmationTemplate.objects.get(id=purchase_confirmation_template.get('id', None))
            else:
                template_set.purchase_confirmation_template = None
        # Deserialize purchase_order_template
        purchase_order_template = validated_data.pop('purchase_order_template')
        if purchase_order_template:
            if purchase_order_template.get('id', None):
                template_set.purchase_order_template = PurchaseOrderTemplate.objects.get(id=purchase_order_template.get('id', None))
            else:
                template_set.purchase_order_template = None
        # Deserialize profit_loss_statement_template
        profit_loss_statement_template = validated_data.pop('profit_loss_statement_template')
        if profit_loss_statement_template:
            if profit_loss_statement_template.get('id', None):
                template_set.profit_loss_statement_template = ProfitLossStatementTemplate.objects.get(id=profit_loss_statement_template.get('id', None))
            else:
                template_set.profit_loss_statement_template = None
        # Deserialize balance_sheet_statement_template
        balance_sheet_statement_template = validated_data.pop('balance_sheet_statement_template')
        if balance_sheet_statement_template:
            if balance_sheet_statement_template.get('id', None):
                template_set.balance_sheet_statement_template = BalanceSheetTemplate.objects.get(id=balance_sheet_statement_template.get('id', None))
            else:
                template_set.balance_sheet_statement_template = None
        # Deserialize monthly_project_summary_template
        monthly_project_summary_template = validated_data.pop('monthly_project_summary_template')
        if monthly_project_summary_template:
            if monthly_project_summary_template.get('id', None):
                template_set.monthly_project_summary_template = MonthlyProjectSummaryTemplate.objects.get(id=monthly_project_summary_template.get('id', None))
            else:
                template_set.monthly_project_summary_template = None
        # Deserialize work_report_template
        work_report_template = validated_data.pop('work_report_template')
        if work_report_template:
            if work_report_template.get('id', None):
                template_set.work_report_template = WorkReportTemplate.objects.get(id=work_report_template.get('id', None))
            else:
                template_set.work_report_template = None
        template_set.save()

    def update(self, template_set, validated_data):
        # Deserialize invoice template
        invoice_template = validated_data.pop('invoice_template')
        if invoice_template:
            if invoice_template.get('id', None):
                template_set.invoice_template = InvoiceTemplate.objects.get(id=invoice_template.get('id', None))
            else:
                template_set.invoice_template = template_set.invoice_template_id
        else:
            template_set.invoice_template = None
        # Deserialize quote template
        quote_template = validated_data.pop('quote_template')
        if quote_template:
            if quote_template.get('id', None):
                template_set.quote_template = QuoteTemplate.objects.get(id=quote_template.get('id', None))
            else:
                template_set.quote_template = template_set.quote_template_id
        else:
            template_set.quote_template = None
        # Deserialize delivery note template
        delivery_note_template = validated_data.pop('delivery_note_template')
        if delivery_note_template:
            if delivery_note_template.get('id', None):
                template_set.delivery_note_template = DeliveryNoteTemplate.objects.get(id=delivery_note_template.get('id', None))
            else:
                template_set.delivery_note_template = template_set.delivery_note_template_id
        else:
            template_set.delivery_note_template = None
        # Deserialize payment reminder template
        payment_reminder_template = validated_data.pop('payment_reminder_template')
        if payment_reminder_template:
            if payment_reminder_template.get('id', None):
                template_set.payment_reminder_template = PaymentReminderTemplate.objects.get(id=payment_reminder_template.get('id', None))
            else:
                template_set.payment_reminder_template = template_set.payment_reminder_template_id
        else:
            template_set.payment_reminder_template = None
        # Deserialize purchase_confirmation_template
        purchase_confirmation_template = validated_data.pop('purchase_confirmation_template')
        if purchase_confirmation_template:
            if purchase_confirmation_template.get('id', None):
                template_set.purchase_confirmation_template = PurchaseConfirmationTemplate.objects.get(id=purchase_confirmation_template.get('id', None))
            else:
                template_set.purchase_confirmation_template = template_set.purchase_confirmation_template_id
        else:
            template_set.purchase_confirmation_template = None
        # Deserialize purchase_order_template
        purchase_order_template = validated_data.pop('purchase_order_template')
        if purchase_order_template:
            if purchase_order_template.get('id', None):
                template_set.purchase_order_template = PurchaseOrderTemplate.objects.get(id=purchase_order_template.get('id', None))
            else:
                template_set.purchase_order_template = template_set.purchase_order_template_id
        else:
            template_set.purchase_order_template = None
        # Deserialize profit_loss_statement_template
        profit_loss_statement_template = validated_data.pop('profit_loss_statement_template')
        if profit_loss_statement_template:
            if profit_loss_statement_template.get('id', None):
                template_set.profit_loss_statement_template = ProfitLossStatementTemplate.objects.get(id=profit_loss_statement_template.get('id', None))
            else:
                template_set.profit_loss_statement_template = template_set.profit_loss_statement_template_id
        else:
            template_set.profit_loss_statement_template = None
        # Deserialize balance_sheet_statement_template
        balance_sheet_statement_template = validated_data.pop('balance_sheet_statement_template')
        if balance_sheet_statement_template:
            if balance_sheet_statement_template.get('id', None):
                template_set.balance_sheet_statement_template = BalanceSheetTemplate.objects.get(id=balance_sheet_statement_template.get('id', None))
            else:
                template_set.balance_sheet_statement_template = template_set.balance_sheet_statement_template_id
        else:
            template_set.balance_sheet_statement_template = None
        # Deserialize monthly_project_summary_template
        monthly_project_summary_template = validated_data.pop('monthly_project_summary_template')
        if monthly_project_summary_template:
            if monthly_project_summary_template.get('id', None):
                template_set.monthly_project_summary_template = MonthlyProjectSummaryTemplate.objects.get(id=monthly_project_summary_template.get('id', None))
            else:
                template_set.monthly_project_summary_template = template_set.monthly_project_summary_template_id
        else:
            template_set.monthly_project_summary_template = None
        # Deserialize work_report_template
        work_report_template = validated_data.pop('work_report_template')
        if work_report_template:
            if work_report_template.get('id', None):
                template_set.work_report_template = WorkReportTemplate.objects.get(id=work_report_template.get('id', None))
            else:
                template_set.work_report_template = template_set.work_report_template_id
        else:
            template_set.work_report_template = None
        template_set.save()
