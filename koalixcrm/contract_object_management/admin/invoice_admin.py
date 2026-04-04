# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.contrib.admin import helpers
from django.shortcuts import render
from django.contrib import messages
from django.template.context_processors import csrf
from koalixcrm.plugin import *
from koalixcrm.contract_object_management.models.invoice import Invoice
from koalixcrm.contract_object_management.admin.sales_document_admin import OptionSalesDocument
from koalixcrm.accounting.models import Account


class OptionInvoice(OptionSalesDocument):
    list_display = OptionSalesDocument.list_display + ('payable_until', 'status',)
    list_filter = OptionSalesDocument.list_filter + ('status',)
    ordering = OptionSalesDocument.ordering
    search_fields = OptionSalesDocument.search_fields
    fieldsets = OptionSalesDocument.fieldsets + (
        (_('Invoice specific'), {
            'fields': ('payable_until', 'status', 'payment_bank_reference' )
        }),
    )

    class PaymentForm(forms.Form):
        payment_amount = forms.DecimalField()
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        payment_account = forms.ModelChoiceField(Account.objects.filter(account_type="A"))

    def register_invoice_in_accounting(self, request, queryset):
        from koalixcrm.crm.exceptions import OpenInterestAccountMissing, IncompleteInvoice
        try:
            for obj in queryset:
                obj.register_invoice_in_accounting(request)
            self.message_user(request, _("Successfully registered Invoice in the Accounting"))
            return
        except OpenInterestAccountMissing as e:
            self.message_user(request, "Did not register Invoice in Accounting: " + e.__str__(), level=messages.ERROR)
            return
        except IncompleteInvoice as e:
            self.message_user(request, "Did not register Invoice in Accounting: " + e.__str__(), level=messages.ERROR)
            return

    register_invoice_in_accounting.short_description = _("Register Invoice in Accounting")

    def register_payment_in_accounting(self, request, queryset):
        form = None
        if request.POST.get('post'):
            if 'cancel' in request.POST:
                self.message_user(request, _("Canceled registration of payment in the accounting"), level=messages.ERROR)
                return
            elif 'register' in request.POST:
                form = self.PaymentForm(request.POST)
                if form.is_valid():
                    payment_amount = form.cleaned_data['payment_amount']
                    payment_account = form.cleaned_data['payment_account']
                    for obj in queryset:
                        obj.register_payment_in_accounting(request, payment_amount, payment_account)
                    self.message_user(request, _("Successfully registered Payment in the Accounting"))
                    return HttpResponseRedirect(request.get_full_path())
        else:
            form = self.PaymentForm
            c = {'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                 'queryset': queryset,
                 'form': form}
            c.update(csrf(request))
            return render(request, 'crm/admin/register_payment.html', c)

    register_payment_in_accounting.short_description = _("Register Payment in Accounting")

    save_as = OptionSalesDocument.save_as
    inlines = OptionSalesDocument.inlines

    actions = ['create_purchase_confirmation',
               'create_quote',
               'create_invoice',
               'create_delivery_note',
               'create_purchase_order',
               'create_payment_reminder',
               'create_pdf',
               'register_invoice_in_accounting',
               'register_payment_in_accounting',]

    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("invoiceActions"))
    inlines.extend(pluginProcessor.getPluginAdditions("invoiceInlines"))


class InlineInvoice(admin.TabularInline):
    model = Invoice
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = ('link_to_invoice',
                       'contract',
                       'customer',
                       'payable_until',
                       'status',
                       'last_pricing_date',
                       'last_calculated_price',
                       'last_calculated_tax')
    fieldsets = (
        (_('Invoice'), {
            'fields': ('link_to_invoice',
                       'contract',
                       'customer',
                       'payable_until',
                       'status',
                       'last_pricing_date',
                       'last_calculated_price',
                       'last_calculated_tax')
        }),
    )

    allow_add = False
