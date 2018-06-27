# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.djangoUserExtension.models import *


class InlineUserExtensionPostalAddress(admin.StackedInline):
    model = UserExtensionPostalAddress
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        (_('Basics'), {
            'fields': (
            'prefix', 'prename', 'name', 'addressline1', 'addressline2',
            'addressline3', 'addressline4', 'zipcode',
            'town', 'state', 'country', 'purpose')
        }),
    )
    allow_add = True


class InlineUserExtensionPhoneAddress(admin.StackedInline):
    model = UserExtensionPhoneAddress
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('phone', 'purpose',)
        }),
    )
    allow_add = True


class InlineUserExtensionEmailAddress(admin.StackedInline):
    model = UserExtensionEmailAddress
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('email', 'purpose',)
        }),
    )
    allow_add = True


class InlineTextParagraph(admin.TabularInline):
    model = TextParagraphInDocumentTemplate
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('purpose', 'text_paragraph',)
        }),
    )
    allow_add = True


class OptionUserExtension(admin.ModelAdmin):
    list_display = ('id', 'user', 'defaultTemplateSet', 'defaultCurrency')
    list_display_links = ('id', 'user')
    list_filter = ('user', 'defaultTemplateSet',)
    ordering = ('id',)
    search_fields = ('id', 'user')
    fieldsets = (
        (_('Basics'), {
            'fields': ('user', 'defaultTemplateSet', 'defaultCurrency')
        }),
    )
    save_as = True
    inlines = [InlineUserExtensionPostalAddress, InlineUserExtensionPhoneAddress, InlineUserExtensionEmailAddress]


class OptionTemplateSet(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'invoice_template', 'quote_template',
                     'delivery_note_template', 'payment_reminder_template',
                     'purchase_confirmation_template', 'purchase_order_template',
                     'profit_loss_statement_template', 'balance_sheet_statement_template',
                     'monthly_project_summary_template')
        }),
    )


class OptionInvoiceTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xsl_file', 'fop_config_file', 'logo')
        }),
    )
    inlines = [InlineTextParagraph]


class OptionQuoteTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xsl_file', 'fop_config_file', 'logo')
        }),
    )
    inlines = [InlineTextParagraph]


class OptionDeliveryNoteTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xsl_file', 'fop_config_file', 'logo')
        }),
    )
    inlines = [InlineTextParagraph]


class OptionPaymentReminderTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xsl_file', 'fop_config_file', 'logo')
        }),
    )
    inlines = [InlineTextParagraph]


class OptionPurchaseOrderTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xsl_file', 'fop_config_file', 'logo')
        }),
    )
    inlines = [InlineTextParagraph]


class OptionPurchaseConfirmationTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xsl_file', 'fop_config_file', 'logo')
        }),
    )
    inlines = [InlineTextParagraph]


class OptionProfitLossStatementTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xsl_file', 'fop_config_file', 'logo')
        }),
    )
    inlines = [InlineTextParagraph]


class OptionBalanceSheetTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xsl_file', 'fop_config_file', 'logo')
        }),
    )
    inlines = [InlineTextParagraph]


class OptionProjectSummaryTemplate(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    search_fields = ('id', 'title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xsl_file', 'fop_config_file', 'logo')
        }),
    )
    inlines = [InlineTextParagraph]

admin.site.register(UserExtension, OptionUserExtension)
admin.site.register(TemplateSet, OptionTemplateSet)
admin.site.register(InvoiceTemplate, OptionInvoiceTemplate)
admin.site.register(QuoteTemplate, OptionQuoteTemplate)
admin.site.register(DeliveryNoteTemplate, OptionDeliveryNoteTemplate)
admin.site.register(PaymentReminderTemplate, OptionPaymentReminderTemplate)
admin.site.register(PurchaseOrderTemplate, OptionPurchaseOrderTemplate)
admin.site.register(PurchaseConfirmationTemplate, OptionPurchaseConfirmationTemplate)
admin.site.register(ProfitLossStatementTemplate, OptionProfitLossStatementTemplate)
admin.site.register(BalanceSheetTemplate, OptionBalanceSheetTemplate)
admin.site.register(MonthlyProjectSummaryTemplate, OptionProjectSummaryTemplate)
