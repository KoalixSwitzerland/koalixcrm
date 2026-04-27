from rest_framework import serializers

from koalixcrm.djangoUserExtension.models.document_template import (
    BalanceSheetTemplate,
    DespatchAdviceTemplate,
    InvoiceTemplate,
    MonthlyProjectSummaryTemplate,
    PaymentReminderTemplate,
    ProfitLossStatementTemplate,
    PurchaseOrderTemplate,
    QuotationTemplate,
    SalesOrderTemplate,
    WorkReportTemplate,
)
from koalixcrm.djangoUserExtension.models.template_set import TemplateSet
from koalixcrm.djangoUserExtension.serializers.document_template_rest import (
    OptionBalanceSheetTemplateJSONSerializer,
    OptionDespatchAdviceTemplateJSONSerializer,
    OptionInvoiceTemplateJSONSerializer,
    OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer,
    OptionPaymentReminderTemplateJSONSerializer,
    OptionProfitLossStatementTemplateJSONSerializer,
    OptionPurchaseOrderTemplateJSONSerializer,
    OptionQuotationTemplateJSONSerializer,
    OptionSalesOrderTemplateJSONSerializer,
    OptionWorkReportTemplateJSONSerializer,
)


class OptionTemplateSetJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    invoice_template = OptionInvoiceTemplateJSONSerializer(read_only=True)
    quotation_template = OptionQuotationTemplateJSONSerializer(read_only=True)
    despatch_advice_template = OptionDespatchAdviceTemplateJSONSerializer(read_only=True)
    payment_reminder_template = OptionPaymentReminderTemplateJSONSerializer(read_only=True)
    sales_order_template = OptionSalesOrderTemplateJSONSerializer(read_only=True)
    purchase_order_template = OptionPurchaseOrderTemplateJSONSerializer(read_only=True)
    profit_loss_statement_template = OptionProfitLossStatementTemplateJSONSerializer(read_only=True)
    balance_sheet_statement_template = OptionBalanceSheetTemplateJSONSerializer(read_only=True)
    monthly_project_summary_template = OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer(read_only=True)
    work_report_template = OptionWorkReportTemplateJSONSerializer(read_only=True)

    class Meta:
        model = TemplateSet
        fields = (
            "id",
            "title",
            "invoice_template",
            "quotation_template",
            "despatch_advice_template",
            "payment_reminder_template",
            "sales_order_template",
            "purchase_order_template",
            "profit_loss_statement_template",
            "balance_sheet_statement_template",
            "monthly_project_summary_template",
            "work_report_template",
        )


class TemplateSetJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    invoice_template = OptionInvoiceTemplateJSONSerializer(required=False, allow_null=True)
    quotation_template = OptionQuotationTemplateJSONSerializer(required=False, allow_null=True)
    despatch_advice_template = OptionDespatchAdviceTemplateJSONSerializer(required=False, allow_null=True)
    payment_reminder_template = OptionPaymentReminderTemplateJSONSerializer(required=False, allow_null=True)
    sales_order_template = OptionSalesOrderTemplateJSONSerializer(required=False, allow_null=True)
    purchase_order_template = OptionPurchaseOrderTemplateJSONSerializer(required=False, allow_null=True)
    profit_loss_statement_template = OptionProfitLossStatementTemplateJSONSerializer(required=False, allow_null=True)
    balance_sheet_statement_template = OptionBalanceSheetTemplateJSONSerializer(required=False, allow_null=True)
    monthly_project_summary_template = OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer(
        required=False, allow_null=True
    )
    work_report_template = OptionWorkReportTemplateJSONSerializer(required=False, allow_null=True)

    class Meta:
        model = TemplateSet
        fields = (
            "id",
            "title",
            "invoice_template",
            "quotation_template",
            "despatch_advice_template",
            "payment_reminder_template",
            "sales_order_template",
            "purchase_order_template",
            "profit_loss_statement_template",
            "balance_sheet_statement_template",
            "monthly_project_summary_template",
            "work_report_template",
        )

    def create(self, validated_data):
        template_set = TemplateSet()
        # Deserialize invoice template
        invoice_template = validated_data.pop("invoice_template")
        if invoice_template:
            if invoice_template.get("id", None):
                template_set.invoice_template = InvoiceTemplate.objects.get(id=invoice_template.get("id", None))
            else:
                template_set.invoice_template = None
        # Deserialize quotation template
        quotation_template = validated_data.pop("quotation_template")
        if quotation_template:
            if quotation_template.get("id", None):
                template_set.quotation_template = QuotationTemplate.objects.get(id=quotation_template.get("id", None))
            else:
                template_set.quotation_template = None
        # Deserialize despatch advice template
        despatch_advice_template = validated_data.pop("despatch_advice_template")
        if despatch_advice_template:
            if despatch_advice_template.get("id", None):
                template_set.despatch_advice_template = DespatchAdviceTemplate.objects.get(
                    id=despatch_advice_template.get("id", None)
                )
            else:
                template_set.despatch_advice_template = None
        # Deserialize payment reminder template
        payment_reminder_template = validated_data.pop("payment_reminder_template")
        if payment_reminder_template:
            if payment_reminder_template.get("id", None):
                template_set.payment_reminder_template = PaymentReminderTemplate.objects.get(
                    id=payment_reminder_template.get("id", None)
                )
            else:
                template_set.payment_reminder_template = None
        # Deserialize sales_order_template
        sales_order_template = validated_data.pop("sales_order_template")
        if sales_order_template:
            if sales_order_template.get("id", None):
                template_set.sales_order_template = SalesOrderTemplate.objects.get(
                    id=sales_order_template.get("id", None)
                )
            else:
                template_set.sales_order_template = None
        # Deserialize purchase_order_template
        purchase_order_template = validated_data.pop("purchase_order_template")
        if purchase_order_template:
            if purchase_order_template.get("id", None):
                template_set.purchase_order_template = PurchaseOrderTemplate.objects.get(
                    id=purchase_order_template.get("id", None)
                )
            else:
                template_set.purchase_order_template = None
        # Deserialize profit_loss_statement_template
        profit_loss_statement_template = validated_data.pop("profit_loss_statement_template")
        if profit_loss_statement_template:
            if profit_loss_statement_template.get("id", None):
                template_set.profit_loss_statement_template = ProfitLossStatementTemplate.objects.get(
                    id=profit_loss_statement_template.get("id", None)
                )
            else:
                template_set.profit_loss_statement_template = None
        # Deserialize balance_sheet_statement_template
        balance_sheet_statement_template = validated_data.pop("balance_sheet_statement_template")
        if balance_sheet_statement_template:
            if balance_sheet_statement_template.get("id", None):
                template_set.balance_sheet_statement_template = BalanceSheetTemplate.objects.get(
                    id=balance_sheet_statement_template.get("id", None)
                )
            else:
                template_set.balance_sheet_statement_template = None
        # Deserialize monthly_project_summary_template
        monthly_project_summary_template = validated_data.pop("monthly_project_summary_template")
        if monthly_project_summary_template:
            if monthly_project_summary_template.get("id", None):
                template_set.monthly_project_summary_template = MonthlyProjectSummaryTemplate.objects.get(
                    id=monthly_project_summary_template.get("id", None)
                )
            else:
                template_set.monthly_project_summary_template = None
        # Deserialize work_report_template
        work_report_template = validated_data.pop("work_report_template")
        if work_report_template:
            if work_report_template.get("id", None):
                template_set.work_report_template = WorkReportTemplate.objects.get(
                    id=work_report_template.get("id", None)
                )
            else:
                template_set.work_report_template = None
        template_set.save()

    def update(self, template_set, validated_data):
        # Deserialize invoice template
        invoice_template = validated_data.pop("invoice_template")
        if invoice_template:
            if invoice_template.get("id", None):
                template_set.invoice_template = InvoiceTemplate.objects.get(id=invoice_template.get("id", None))
            else:
                template_set.invoice_template = template_set.invoice_template_id
        else:
            template_set.invoice_template = None
        # Deserialize quotation template
        quotation_template = validated_data.pop("quotation_template")
        if quotation_template:
            if quotation_template.get("id", None):
                template_set.quotation_template = QuotationTemplate.objects.get(id=quotation_template.get("id", None))
            else:
                template_set.quotation_template = template_set.quotation_template_id
        else:
            template_set.quotation_template = None
        # Deserialize despatch advice template
        despatch_advice_template = validated_data.pop("despatch_advice_template")
        if despatch_advice_template:
            if despatch_advice_template.get("id", None):
                template_set.despatch_advice_template = DespatchAdviceTemplate.objects.get(
                    id=despatch_advice_template.get("id", None)
                )
            else:
                template_set.despatch_advice_template = template_set.despatch_advice_template_id
        else:
            template_set.despatch_advice_template = None
        # Deserialize payment reminder template
        payment_reminder_template = validated_data.pop("payment_reminder_template")
        if payment_reminder_template:
            if payment_reminder_template.get("id", None):
                template_set.payment_reminder_template = PaymentReminderTemplate.objects.get(
                    id=payment_reminder_template.get("id", None)
                )
            else:
                template_set.payment_reminder_template = template_set.payment_reminder_template_id
        else:
            template_set.payment_reminder_template = None
        # Deserialize sales_order_template
        sales_order_template = validated_data.pop("sales_order_template")
        if sales_order_template:
            if sales_order_template.get("id", None):
                template_set.sales_order_template = SalesOrderTemplate.objects.get(
                    id=sales_order_template.get("id", None)
                )
            else:
                template_set.sales_order_template = template_set.sales_order_template_id
        else:
            template_set.sales_order_template = None
        # Deserialize purchase_order_template
        purchase_order_template = validated_data.pop("purchase_order_template")
        if purchase_order_template:
            if purchase_order_template.get("id", None):
                template_set.purchase_order_template = PurchaseOrderTemplate.objects.get(
                    id=purchase_order_template.get("id", None)
                )
            else:
                template_set.purchase_order_template = template_set.purchase_order_template_id
        else:
            template_set.purchase_order_template = None
        # Deserialize profit_loss_statement_template
        profit_loss_statement_template = validated_data.pop("profit_loss_statement_template")
        if profit_loss_statement_template:
            if profit_loss_statement_template.get("id", None):
                template_set.profit_loss_statement_template = ProfitLossStatementTemplate.objects.get(
                    id=profit_loss_statement_template.get("id", None)
                )
            else:
                template_set.profit_loss_statement_template = template_set.profit_loss_statement_template_id
        else:
            template_set.profit_loss_statement_template = None
        # Deserialize balance_sheet_statement_template
        balance_sheet_statement_template = validated_data.pop("balance_sheet_statement_template")
        if balance_sheet_statement_template:
            if balance_sheet_statement_template.get("id", None):
                template_set.balance_sheet_statement_template = BalanceSheetTemplate.objects.get(
                    id=balance_sheet_statement_template.get("id", None)
                )
            else:
                template_set.balance_sheet_statement_template = template_set.balance_sheet_statement_template_id
        else:
            template_set.balance_sheet_statement_template = None
        # Deserialize monthly_project_summary_template
        monthly_project_summary_template = validated_data.pop("monthly_project_summary_template")
        if monthly_project_summary_template:
            if monthly_project_summary_template.get("id", None):
                template_set.monthly_project_summary_template = MonthlyProjectSummaryTemplate.objects.get(
                    id=monthly_project_summary_template.get("id", None)
                )
            else:
                template_set.monthly_project_summary_template = template_set.monthly_project_summary_template_id
        else:
            template_set.monthly_project_summary_template = None
        # Deserialize work_report_template
        work_report_template = validated_data.pop("work_report_template")
        if work_report_template:
            if work_report_template.get("id", None):
                template_set.work_report_template = WorkReportTemplate.objects.get(
                    id=work_report_template.get("id", None)
                )
            else:
                template_set.work_report_template = template_set.work_report_template_id
        else:
            template_set.work_report_template = None
        template_set.save()
