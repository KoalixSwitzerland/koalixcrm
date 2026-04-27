# -*- coding: utf-8 -*-

from django import forms
from django.apps import apps
from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.utils.translation import gettext as _

from koalixcrm.contracts.admin.commercial_document_admin import OptionCommercialDocument
from koalixcrm.contracts.models.invoice import Invoice
from koalixcrm.plugin import *


def _activa_account_queryset():
    """Queryset of accounting.Account rows of type 'A' (activa).

    Returns an empty queryset when the accounting app is not installed, so
    the PaymentForm stays constructible in a WFS deployment."""
    if not apps.is_installed("koalixcrm.accounting"):
        return ()
    account_model = apps.get_model("accounting", "Account")
    return account_model.objects.filter(account_type="A")


class OptionInvoice(OptionCommercialDocument):
    list_display = OptionCommercialDocument.list_display + (
        "payable_until",
        "status",
    )
    list_filter = OptionCommercialDocument.list_filter + ("status",)
    ordering = OptionCommercialDocument.ordering
    search_fields = OptionCommercialDocument.search_fields
    fieldsets = OptionCommercialDocument.fieldsets + (
        (_("Invoice specific"), {"fields": ("payable_until", "status", "payment_bank_reference")}),
    )

    class PaymentForm(forms.Form):
        payment_amount = forms.DecimalField()
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        payment_account = forms.ModelChoiceField(queryset=None)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["payment_account"].queryset = _activa_account_queryset()

    def register_invoice_in_accounting(self, request, queryset):
        from koalixcrm.core.exceptions import (
            IncompleteInvoice,
            OpenInterestAccountMissing,
        )

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
        if request.POST.get("post"):
            if "cancel" in request.POST:
                self.message_user(
                    request, _("Canceled registration of payment in the accounting"), level=messages.ERROR
                )
                return
            elif "register" in request.POST:
                form = self.PaymentForm(request.POST)
                if form.is_valid():
                    payment_amount = form.cleaned_data["payment_amount"]
                    payment_account = form.cleaned_data["payment_account"]
                    for obj in queryset:
                        obj.register_payment_in_accounting(request, payment_amount, payment_account)
                    self.message_user(request, _("Successfully registered Payment in the Accounting"))
                    return HttpResponseRedirect(request.get_full_path())
        else:
            form = self.PaymentForm
            c = {"action_checkbox_name": helpers.ACTION_CHECKBOX_NAME, "queryset": queryset, "form": form}
            c.update(csrf(request))
            return render(request, "crm/admin/register_payment.html", c)

    register_payment_in_accounting.short_description = _("Register Payment in Accounting")

    def create_credit_note_from_invoice(self, request, queryset):
        import koalixcrm.contracts.models.credit_note
        from koalixcrm.contracts.views.newdocument import CreateNewDocumentView

        for obj in queryset:
            response = CreateNewDocumentView.create_new_document(
                self,
                request,
                obj,
                koalixcrm.contracts.models.credit_note.CreditNote,
                ("/admin/contract_object_management/" + obj.__class__.__name__.lower() + "/"),
            )
            return response

    create_credit_note_from_invoice.short_description = _("Create Credit Note from Invoice")

    save_as = OptionCommercialDocument.save_as
    inlines = OptionCommercialDocument.inlines

    actions = [
        "create_sales_order",
        "create_quotation",
        "create_invoice",
        "create_despatch_advice",
        "create_purchase_order",
        "create_payment_reminder",
        "create_pdf_async",
        "create_credit_note_from_invoice",
    ]
    if apps.is_installed("koalixcrm.accounting"):
        actions = actions + ["register_invoice_in_accounting", "register_payment_in_accounting"]

    pluginProcessor = PluginProcessor()
    actions.extend(pluginProcessor.getPluginAdditions("invoiceActions"))
    inlines.extend(pluginProcessor.getPluginAdditions("invoiceInlines"))


class InlineInvoice(admin.TabularInline):
    model = Invoice
    classes = ["collapse"]
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = (
        "link_to_invoice",
        "contract",
        "party",
        "payable_until",
        "status",
        "last_pricing_date",
        "last_calculated_price",
        "last_calculated_tax",
    )
    fieldsets = (
        (
            _("Invoice"),
            {
                "fields": (
                    "link_to_invoice",
                    "contract",
                    "party",
                    "payable_until",
                    "status",
                    "last_pricing_date",
                    "last_calculated_price",
                    "last_calculated_tax",
                )
            },
        ),
    )

    allow_add = False
