# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext as _
from apps.accounting.views import *


class AccountingPeriodBooking(admin.TabularInline):
    model = Booking
    extra = 1
    show_change_link = True
    can_delete = True
    classes = ['collapse']
    fields = ('fromAccount', 'toAccount', 'description', 'amount', 'bookingDateOnly', 'staff', 'bookingReference',)
    readonly_fields = (
    'fromAccount', 'toAccount', 'description', 'amount', 'bookingDateOnly', 'staff', 'bookingReference',)
    allow_add = True


class OptionBooking(admin.ModelAdmin):
    list_display = ('fromAccount', 'toAccount', 'amount', 'bookingDateOnly', 'staff')
    fieldsets = ((_('Basic'), {'fields': (
    'fromAccount', 'toAccount', 'amount', 'bookingDate', 'staff', 'description', 'bookingReference',
    'accountingPeriod')}),)
    save_as = True

    def save_model(self, request, obj, form, change):
        if (change == True):
            obj.lastmodifiedby = request.user
        else:
            obj.lastmodifiedby = request.user
            obj.staff = request.user
        obj.save()


class AccountForm(forms.ModelForm):
    """AccountForm is used to overwrite the clean method of the
    original form and to add an additional checks to the model"""

    class Meta:
        model = Account
        fields = '__all__'

    def clean(self):
        super(AccountForm, self).clean()
        errors = []
        if (self.cleaned_data['isopenreliabilitiesaccount']):
            openliabilitiesaccount = Account.objects.filter(isopenreliabilitiesaccount=True)
            if (self.cleaned_data['accountType'] != "L"):
                errors.append(_('The open liabilites account must be a liabities account'))
            elif openliabilitiesaccount:
                errors.append(_('There may only be one open liablities account in the system'))
        if (self.cleaned_data['isopeninterestaccount']):
            openinterestaccounts = Account.objects.filter(isopeninterestaccount=True)
            if (self.cleaned_data['accountType'] != "A"):
                errors.append(_('The open intrests account must be an asset account'))
            elif openinterestaccounts:
                errors.append(_('There may only be one open intrests account in the system'))
        if (self.cleaned_data['isACustomerPaymentAccount']):
            if (self.cleaned_data['accountType'] != "A"):
                errors.append(_('A customer payment account must be an asset account'))
        if (self.cleaned_data['isProductInventoryActiva']):
            if (self.cleaned_data['accountType'] != "A"):
                errors.append(_('A product inventory account must be an asset account'))
        if len(errors) > 0:
            raise forms.ValidationError(errors)
        return self.cleaned_data


class OptionAccount(admin.ModelAdmin):
    list_display = ('accountNumber', 'accountType', 'title', 'sumOfAllBookings')
    list_display_links = ('accountNumber', 'accountType', 'title', 'sumOfAllBookings')
    fieldsets = ((_('Basic'), {'fields': (
    'accountNumber', 'accountType', 'title', 'description', 'isopenreliabilitiesaccount', 'isopeninterestaccount',
    'isProductInventoryActiva', 'isACustomerPaymentAccount')}),)
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
    list_display = ('title', 'begin', 'end')
    list_display_links = ('title', 'begin', 'end')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'begin', 'end')
        }),
    )
    inlines = [AccountingPeriodBooking, ]
    save_as = True

    form = AccountingPeriodForm

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if (change == True):
                instance.lastmodifiedby = request.user
            else:
                instance.lastmodifiedby = request.user
                instance.staff = request.user
            instance.save()

    def createBalanceSheet(self, request, queryset):
        for obj in queryset:
            response = exportPDF(self, request, obj, "balanceSheet", "/admin/accounting/accountingperiod/")
            return response

    createBalanceSheet.short_description = _("Create PDF of Balance Sheet")

    def createProfitLossStatement(self, request, queryset):
        for obj in queryset:
            response = exportPDF(self, request, obj, "profitLossStatement", "/admin/accounting/accountingperiod/")
            return response

    createProfitLossStatement.short_description = _("Create PDF of Profit Loss Statement Sheet")

    def exportAllAccounts(self, request, queryset):
        for obj in queryset:
            response = exportXML(self, request, obj, "allAccount", "/admin/accounting/accountingperiod/")
            return response

    exportAllAccounts.short_description = _("Create XML of all Accounts")

    actions = ['createBalanceSheet', 'createProfitLossStatement', 'exportAllAccounts', ]


class OptionProductCategorie(admin.ModelAdmin):
    list_display = ('title', 'profitAccount', 'lossAccount')
    list_display_links = ('title', 'profitAccount', 'lossAccount')
    fieldsets = (
        (_('Basics'), {
            'fields': ('title', 'profitAccount', 'lossAccount')
        }),
    )
    save_as = True


admin.site.register(Account, OptionAccount)
admin.site.register(Booking, OptionBooking)
admin.site.register(ProductCategorie, OptionProductCategorie)
admin.site.register(AccountingPeriod, OptionAccountingPeriod)
