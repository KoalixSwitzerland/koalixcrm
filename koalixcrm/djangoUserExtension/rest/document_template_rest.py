from rest_framework import serializers

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


class OptionDocumentTemplateJSONSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(source='title', required=False, read_only=True)
    xsl_file = serializers.FilePathField(source='xsl_file', read_only=True)
    fop_config_file = serializers.FilePathField(source='user',read_only=True)
    logo = serializers.FilePathField(source='logo', read_only=True)


class OptionInvoiceTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = InvoiceTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionQuoteTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = QuoteTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionDeliveryNoteTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = DeliveryNoteTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionPaymentReminderTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = PaymentReminderTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionPurchaseOrderTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = PurchaseOrderTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionPurchaseConfirmationTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = PurchaseConfirmationTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionProfitLossStatementTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = ProfitLossStatementTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionBalanceSheetTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = BalanceSheetTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = MonthlyProjectSummaryTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')


class OptionWorkReportTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = WorkReportTemplate
        fields = ('title',
                  'xsl_file',
                  'fop_config_file',
                  'logo')
