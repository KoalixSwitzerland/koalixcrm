# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext as _
from koalixcrm.accounting.views import *


class OptionBooking(admin.ModelAdmin):
    list_display = ('from_account',
                    'to_account',
                    'amount',
                    'booking_date_only',
                    'staff')
    fieldsets = ((_('Basic'), {'fields': ('from_account',
                                          'to_account',
                                          'amount',
                                          'booking_date',
                                          'staff',
                                          'description',
                                          'booking_reference',
                                          'accounting_period')}),)
    save_as = True

    def save_model(self, request, obj, form, change):
        if change:
            obj.last_modified_by = request.user
        else:
            obj.last_modified_by = request.user
            obj.staff = request.user
        obj.save()


class InlineBookings(admin.TabularInline):
    model = Booking
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('Basics', {
            'fields': ('from_account',
                       'to_account',
                       'description',
                       'amount',
                       'booking_date',
                       'staff',
                       'booking_reference',)
        }),
    )
    allow_add = False


class AccountForm(forms.ModelForm):
    """AccountForm is used to overwrite the clean method of the
    original form and to add an additional checks to the model"""

    class Meta:
        model = Account
        fields = '__all__'

    def clean(self):
        super(AccountForm, self).clean()
        errors = []
        if (self.cleaned_data['is_open_reliabilities_account']):
            open_reliabilities_account = Account.objects.filter(is_open_reliabilities_account=True)
            if (self.cleaned_data['account_type'] != "L"):
                errors.append(_('The open liabilites account must be a liabities account'))
            elif open_reliabilities_account:
                errors.append(_('There may only be one open liablities account in the system'))
        if (self.cleaned_data['is_open_interest_account']):
            open_interest_account = Account.objects.filter(is_open_interest_account=True)
            if (self.cleaned_data['account_type'] != "A"):
                errors.append(_('The open intrests account must be an asset account'))
            elif open_interest_account:
                errors.append(_('There may only be one open intrests account in the system'))
        if (self.cleaned_data['is_a_customer_payment_account']):
            if (self.cleaned_data['account_type'] != "A"):
                errors.append(_('A customer payment account must be an asset account'))
        if (self.cleaned_data['is_product_inventory_activa']):
            if (self.cleaned_data['account_type'] != "A"):
                errors.append(_('A product inventory account must be an asset account'))
        if len(errors) > 0:
            raise forms.ValidationError(errors)
        return self.cleaned_data


class OptionAccount(admin.ModelAdmin):
    list_display = ('account_number',
                    'account_type',
                    'title',
                    'sum_of_all_bookings')
    list_display_links = ('account_number',
                          'account_type',
                          'title',
                          'sum_of_all_bookings')
    fieldsets = ((_('Basic'),
                  {'fields': ('account_number',
                              'account_type',
                              'title',
                              'description',
                              'is_open_reliabilities_account',
                              'is_open_interest_account',
                              'is_product_inventory_activa',
                              'is_a_customer_payment_aAccount')}),)
    save_as = True

    form = AccountForm


class AccountingPeriodForm(forms.ModelForm):
    """AccountingPeriodForm is used to overwrite the clean method of the
    original form and to add an additional check to the model"""

    class Meta:
        model = AccountingPeriod
        fields = '__all__'

    def clean(self):
        super(AccountingPeriodForm, self).clean()
        errors = []
        try:
            if self.cleaned_data['begin'] > self.cleaned_data['end']:
                errors.append(_('The begin date cannot be later than the end date.'))
        except KeyError:
            errors.append(_('The begin and the end date may not be empty'))
        if errors:
            raise forms.ValidationError(errors)
        return self.cleaned_data


class OptionAccountingPeriod(admin.ModelAdmin):
    list_display = ('title',
                    'begin',
                    'end',
                    'template_set_balance_sheet',
                    'template_profit_loss_statement')
    list_display_links = ('title',
                          'begin',
                          'end',
                          'template_set_balance_sheet',
                          'template_profit_loss_statement')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title',
                       'begin',
                       'end',
                       'template_set_balance_sheet',
                       'template_profit_loss_statement')
        }),
    )
    inlines = [InlineBookings, ]
    save_as = True

    form = AccountingPeriodForm

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if change:
                instance.last_modified_by = request.user
            else:
                instance.last_modified_by = request.user
                instance.staff = request.user
            instance.save()

    def create_pdf_of_balance_sheet(self, request, queryset):
        from koalixcrm.crm.views.pdfexport import PDFExportView
        for obj in queryset:
            response = PDFExportView.export_pdf(self,
                                                request,
                                                obj,
                                                ("/admin/accounting/"+obj.__class__.__name__.lower()+"/"),
                                                obj.template_set_balance_sheet)
            return response

    create_pdf_of_balance_sheet.short_description = _("Create PDF of Balance Sheet")

    def create_pdf_of_profit_loss_statement(self, request, queryset):
        from koalixcrm.crm.views.pdfexport import PDFExportView
        for obj in queryset:
            response = PDFExportView.export_pdf(self,
                                                request,
                                                obj,
                                                ("/admin/accounting/"+obj.__class__.__name__.lower()+"/"),
                                                obj.template_profit_loss_statement)
            return response

    create_pdf_of_profit_loss_statement.short_description = _("Create PDF of Profit Loss Statement Sheet")

    def exportAllAccounts(self, request, queryset):
        for obj in queryset:
            response = exportXML(self, request, obj, "allAccount", "/admin/accounting/accountingperiod/")
            return response

    exportAllAccounts.short_description = _("Create XML of all Accounts")

    actions = ['create_pdf_of_balance_sheet', 'create_pdf_of_profit_loss_statement', 'exportAllAccounts', ]


class OptionProductCategorie(admin.ModelAdmin):
    list_display = ('title', 'profit_account', 'loss_account')
    list_display_links = ('title', 'profit_account', 'loss_account')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'profit_account', 'loss_account')
        }),
    )
    save_as = True


admin.site.register(Account, OptionAccount)
admin.site.register(Booking, OptionBooking)
admin.site.register(ProductCategorie, OptionProductCategorie)
admin.site.register(AccountingPeriod, OptionAccountingPeriod)
