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
    title = serializers.CharField(required=False, read_only=True)
    xslFile = serializers.FileField(source='xsl_file', read_only=True)
    fopConfigFile = serializers.FileField(source='user', read_only=True)
    logo = serializers.FileField(read_only=True)


class OptionInvoiceTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = InvoiceTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')


class OptionQuoteTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = QuoteTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')


class OptionDeliveryNoteTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = DeliveryNoteTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')


class OptionPaymentReminderTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = PaymentReminderTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')


class OptionPurchaseOrderTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = PurchaseOrderTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')


class OptionPurchaseConfirmationTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = PurchaseConfirmationTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')


class OptionProfitLossStatementTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = ProfitLossStatementTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')


class OptionBalanceSheetTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = BalanceSheetTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')


class OptionMonthlyProjectSummaryTemplateTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = MonthlyProjectSummaryTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')


class OptionWorkReportTemplateJSONSerializer(OptionDocumentTemplateJSONSerializer):
    class Meta:
        model = WorkReportTemplate
        fields = ('title',
                  'xslFile',
                  'fopConfigFile',
                  'logo')
