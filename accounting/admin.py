# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin

from accounting.views import *


class AccountingPeriodBooking(admin.TabularInline):
    model = Booking
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('Basics', {
            'fields': ('fromAccount', 'toAccount', 'description', 'amount', 'bookingDate', 'staff', 'bookingReference',)
        }),
    )
    allow_add = True


class OptionBooking(admin.ModelAdmin):
    list_display = ('fromAccount', 'toAccount', 'amount', 'bookingDate', 'staff')
    fieldsets = ((trans('Basic'), {'fields': (
        'fromAccount', 'toAccount', 'amount', 'bookingDate', 'staff', 'description', 'bookingReference',
        'accountingPeriod')}),)
    save_as = True

    def save_model(self, request, obj, form, change):
        if change:
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()


class AccountForm(forms.ModelForm):
    """ AccountForm is used to overwrite the clean method of the 
    original form and to add an additional checks to the model"""

    class Meta:
        model = Account
        fields = [
            'accountNumber',
            'title',
            'accountType',
            'description',
            'originalAmount',
            'isopenreliabilitiesaccount',
            'isopeninterestaccount',
            'isProductInventoryActiva',
            'isACustomerPaymentAccount'
        ]

    def clean(self):
        super(AccountForm, self).clean()
        errors = []
        if self.cleaned_data['isopenreliabilitiesaccount']:
            open_reliabilities_account = Account.objects.filter(isopenreliabilitiesaccount=True)
            if self.cleaned_data['accountType'] != "L":
                errors.append(trans('The open liabilites account must be a liabities account'))
            elif open_reliabilities_account:
                errors.append(trans('There may only be one open liablities account in the system'))

        if self.cleaned_data['isopeninterestaccount']:
            open_interest_accounts = Account.objects.filter(isopeninterestaccount=True)
            if self.cleaned_data['accountType'] != "A":
                errors.append(trans('The open intrests account must be an asset account'))
            elif open_interest_accounts:
                errors.append(trans('There may only be one open intrests account in the system'))

        if self.cleaned_data['isACustomerPaymentAccount']:
            if self.cleaned_data['accountType'] != "A":
                errors.append(trans('A customer payment account must be an asset account'))

        if self.cleaned_data['isProductInventoryActiva']:
            if self.cleaned_data['accountType'] != "A":
                errors.append(trans('A product inventory account must be an asset account'))

        if len(errors) > 0:
            raise forms.ValidationError(errors)
        return self.cleaned_data


class OptionAccount(admin.ModelAdmin):
    list_display = (
        'accountNumber',
        'accountType',
        'title',
        'isopenreliabilitiesaccount',
        'isopeninterestaccount',
        'isProductInventoryActiva',
        'isACustomerPaymentAccount',
        'value'
    )
    list_display_links = ('accountNumber', 'accountType', 'title', 'value')
    fieldsets = ((trans('Basic'), {'fields': (
        'accountNumber',
        'accountType',
        'title',
        'description',
        'originalAmount',
        'isopenreliabilitiesaccount',
        'isopeninterestaccount',
        'isProductInventoryActiva',
        'isACustomerPaymentAccount'
    )}),)
    save_as = True
    form = AccountForm


class AccountingPeriodForm(forms.ModelForm):
    """ AccountingPeriodForm is used to overwrite the clean method of the 
    original form and to add an additional check to the model"""

    class Meta:
        model = AccountingPeriod
        fields = ['title', 'begin', 'end']

    def clean(self):
        super(AccountingPeriodForm, self).clean()
        errors = []
        try:
            if self.cleaned_data['begin'] > self.cleaned_data['end']:
                errors.append(trans('The begin date cannot be later than the end date.'))
        except KeyError:
            errors.append(trans('The begin and the end date may not be empty'))
        if errors:
            raise forms.ValidationError(errors)
        return self.cleaned_data


class OptionAccountingPeriod(admin.ModelAdmin):
    list_display = ('title', 'begin', 'end')
    list_display_links = ('title', 'begin', 'end')
    fieldsets = (
        (trans('Basics'), {
            'fields': ('title', 'begin', 'end')
        }),
    )
    inlines = [AccountingPeriodBooking, ]
    save_as = True

    form = AccountingPeriodForm

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if change:
                instance.lastmodifiedby = request.user
            else:
                instance.lastmodifiedby = request.user
                instance.staff = request.user
            instance.save()

    def create_balance_sheet(self, request, queryset):
        for obj in queryset:
            response = exportPDF(self, request, obj, "balanceSheet", "/admin/accounting/accountingperiod/")
            return response

    create_balance_sheet.short_description = trans("Create PDF of Balance Sheet")

    def create_profit_loss_statement(self, request, queryset):
        for obj in queryset:
            response = exportPDF(self, request, obj, "profitLossStatement", "/admin/accounting/accountingperiod/")
            return response

    create_profit_loss_statement.short_description = trans("Create PDF of Profit Loss Statement Sheet")

    actions = ['create_balance_sheet', 'create_profit_loss_statement']


class OptionProductCategory(admin.ModelAdmin):
    list_display = ('title', 'profitAccount', 'lossAccount')
    list_display_links = ('title', 'profitAccount', 'lossAccount')
    fieldsets = (
        (trans('Basics'), {
            'fields': ('title', 'profitAccount', 'lossAccount')
        }),
    )
    save_as = True


admin.site.register(Account, OptionAccount)
admin.site.register(Booking, OptionBooking)
admin.site.register(ProductCategory, OptionProductCategory)
admin.site.register(AccountingPeriod, OptionAccountingPeriod)
