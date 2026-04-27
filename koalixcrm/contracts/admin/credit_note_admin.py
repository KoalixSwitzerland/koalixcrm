# -*- coding: utf-8 -*-

from django.contrib import admin, messages
from django.utils.translation import gettext as _

from koalixcrm.contracts.admin.commercial_document_admin import OptionCommercialDocument
from koalixcrm.contracts.models.credit_note import CreditNote


class OptionCreditNote(OptionCommercialDocument):
    list_display = OptionCommercialDocument.list_display + ('issue_date', 'status',)
    list_filter = OptionCommercialDocument.list_filter + ('status',)
    ordering = OptionCommercialDocument.ordering
    search_fields = OptionCommercialDocument.search_fields
    fieldsets = OptionCommercialDocument.fieldsets + (
        (_('Credit Note specific'), {
            'fields': ('corrects_invoice', 'status', 'issue_date', 'reason')
        }),
    )

    def register_credit_note_in_accounting(self, request, queryset):
        from koalixcrm.core.exceptions import (
            IncompleteInvoice,
            OpenInterestAccountMissing,
        )
        try:
            for obj in queryset:
                obj.register_credit_note_in_accounting(request)
            self.message_user(request, _("Successfully registered Credit Note in the Accounting"))
            return
        except OpenInterestAccountMissing as e:
            self.message_user(request, "Did not register Credit Note in Accounting: " + e.__str__(), level=messages.ERROR)
            return
        except IncompleteInvoice as e:
            self.message_user(request, "Did not register Credit Note in Accounting: " + e.__str__(), level=messages.ERROR)
            return

    register_credit_note_in_accounting.short_description = _("Register Credit Note in Accounting")

    save_as = OptionCommercialDocument.save_as
    inlines = OptionCommercialDocument.inlines

    actions = ['create_pdf_async', 'register_credit_note_in_accounting']


class InlineCreditNote(admin.TabularInline):
    model = CreditNote
    classes = ['collapse']
    show_change_link = True
    can_delete = True
    extra = 1
    readonly_fields = ('link_to_credit_note',
                       'contract',
                       'party',
                       'issue_date',
                       'status',
                       'last_pricing_date',
                       'last_calculated_price',
                       'last_calculated_tax')
    fieldsets = (
        (_('Credit Note'), {
            'fields': ('link_to_credit_note',
                       'contract',
                       'party',
                       'issue_date',
                       'status',
                       'last_pricing_date',
                       'last_calculated_price',
                       'last_calculated_tax')
        }),
    )

    allow_add = False
