# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from apps.djangoUserExtension.models import *


class InlineUserExtensionPostalAddress(admin.StackedInline):
    model = UserExtensionPostalAddress
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        (_('Basics'), {
            'fields': (
            'prefix', 'prename', 'name', 'addressline1', 'addressline2', 'addressline3', 'addressline4', 'zipcode',
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
    search_fields = ('id', 'title', 'organisationname', 'invoiceXSLFile', 'quoteXSLFile', 'purchaseconfirmationXSLFile',
                     'deilveryorderXSLFile', 'profitLossStatementXSLFile', 'balancesheetXSLFile',
                     'purchaseorderXSLFile',
                     'logo', 'footerTextsalesorders', 'headerTextsalesorders',
                     'headerTextpurchaseorders', 'footerTextpurchaseorders', 'pagefooterleft', 'pagefootermiddle',
                     'bankingaccountref', 'addresser'
                     )
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'organisationname', 'invoiceXSLFile', 'quoteXSLFile', 'purchaseconfirmationXSLFile',
                       'deilveryorderXSLFile', 'profitLossStatementXSLFile', 'balancesheetXSLFile',
                       'purchaseorderXSLFile',
                       'logo', 'fopConfigurationFile', 'footerTextsalesorders', 'headerTextsalesorders',
                       'headerTextpurchaseorders', 'footerTextpurchaseorders', 'pagefooterleft', 'pagefootermiddle',
                       'bankingaccountref', 'addresser')
        }),
    )


class OptionXSLFile(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ('id',)
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'xslfile',)
        }),
    )
    allow_add = True


admin.site.register(UserExtension, OptionUserExtension)
admin.site.register(TemplateSet, OptionTemplateSet)
admin.site.register(XSLFile, OptionXSLFile)
