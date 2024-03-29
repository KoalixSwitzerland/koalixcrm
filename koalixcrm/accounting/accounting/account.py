# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _
from django import forms

from koalixcrm.accounting.const.accountTypeChoices import *
from koalixcrm.accounting.exceptions import AccountingPeriodNotFound
from koalixcrm.crm.documents.pdf_export import PDFExport


class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    account_number = models.IntegerField(verbose_name=_("Account Number"))
    title = models.CharField(verbose_name=_("Account Title"),
                             max_length=50)
    account_type = models.CharField(verbose_name=_("Account Type"),
                                    max_length=1,
                                    choices=ACCOUNTTYPECHOICES)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    is_open_reliabilities_account = models.BooleanField(verbose_name=_("Is The Open Liabilities Account"))
    is_open_interest_account = models.BooleanField(verbose_name=_("Is The Open Interests Account"))
    is_product_inventory_activa = models.BooleanField(verbose_name=_("Is a Product Inventory Account"))
    is_a_customer_payment_account = models.BooleanField(verbose_name=_("Is a Customer Payment Account"))

    def sum_of_all_bookings(self):
        calculated_sum = self.all_bookings(from_account=False) - self.all_bookings(from_account=True)
        if self.account_type == 'E' or self.account_type == 'L':
            calculated_sum = 0 - calculated_sum
        return calculated_sum

    sum_of_all_bookings.short_description = _("Value")

    def sum_of_all_bookings_within_accounting_period(self, accounting_period):
        calculated_sum = self.all_bookings_within_accounting_period(from_account=False,
                                                                    accounting_period=accounting_period) - \
                         self.all_bookings_within_accounting_period(from_account=True,
                                                                    accounting_period=accounting_period)
        if self.account_type == 'E' or self.account_type == 'L':
            calculated_sum = -calculated_sum
        return calculated_sum

    def sum_of_all_bookings_before_accounting_period(self, current_accounting_period):
        try:
            accounting_periods = current_accounting_period.get_all_prior_accounting_periods()
        except AccountingPeriodNotFound:
            return 0
        sum_of_all_bookings = 0
        for accounting_period in accounting_periods:
            sum_of_all_bookings += self.all_bookings_within_accounting_period(from_account=False,
                                                              accounting_period=accounting_period) - self.all_bookings_within_accounting_period(
                from_account=True, accounting_period=accounting_period)
        if self.account_type == 'E' or self.account_type == 'L':
            sum_of_all_bookings = -sum_of_all_bookings
        return sum_of_all_bookings

    def sum_of_all_bookings_through_now(self, current_accounting_period):
        within_accounting_period = self.sum_of_all_bookings_within_accounting_period(current_accounting_period)
        before_accounting_period = self.sum_of_all_bookings_before_accounting_period(current_accounting_period)
        current_value = within_accounting_period + before_accounting_period
        return current_value

    def all_bookings(self, from_account):
        from koalixcrm.accounting.models import Booking
        sum_all = 0
        if from_account:
            bookings = Booking.objects.filter(from_account=self.id)
        else:
            bookings = Booking.objects.filter(to_account=self.id)

        for booking in list(bookings):
            sum_all += booking.amount

        return sum_all

    def all_bookings_within_accounting_period(self, from_account, accounting_period):
        from koalixcrm.accounting.models import Booking
        sum = 0
        if from_account:
            bookings = Booking.objects.filter(from_account=self.id, accounting_period=accounting_period.id)
        else:
            bookings = Booking.objects.filter(to_account=self.id, accounting_period=accounting_period.id)

        for booking in list(bookings):
            sum += booking.amount

        return sum

    def serialize_to_xml(self, accounting_period):
        objects = [self, ]
        main_xml = PDFExport.write_xml(objects)
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.account']",
                                                       "sum_of_all_bookings_within_accounting_period",
                                                       self.sum_of_all_bookings_within_accounting_period(accounting_period))
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.account']",
                                                       "sum_of_all_bookings_through_now",
                                                       self.sum_of_all_bookings_through_now(accounting_period))
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.account']",
                                                       "sum_of_all_bookings_before_accounting_period",
                                                       self.sum_of_all_bookings_before_accounting_period(accounting_period))
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.account']",
                                                       "sum_of_all_bookings_through_now",
                                                       self.sum_of_all_bookings())
        return main_xml

    def __str__(self):
        return self.account_number.__str__() + " " + self.title

    class Meta:
        app_label = "accounting"
        verbose_name = _('Account')
        verbose_name_plural = _('Account')
        ordering = ['account_number']


class AccountForm(forms.ModelForm):
    """AccountForm is used to overwrite the clean method of the
    original form and to add an additional checks to the model"""

    class Meta:
        model = Account
        fields = '__all__'

    def clean(self):
        super(AccountForm, self).clean()
        errors = []
        if self.cleaned_data['is_open_reliabilities_account']:
            open_reliabilities_account = Account.objects.filter(is_open_reliabilities_account=True)
            if self.cleaned_data['account_type'] != "L":
                errors.append(_('The open liabilities account must be a liabities account'))
            elif open_reliabilities_account:
                errors.append(_('There may only be one open liablities account in the system'))
        if self.cleaned_data['is_open_interest_account']:
            open_interest_account = Account.objects.filter(is_open_interest_account=True)
            if self.cleaned_data['account_type'] != "A":
                errors.append(_('The open interests account must be an asset account'))
            elif open_interest_account:
                errors.append(_('There may only be one open intrests account in the system'))
        if self.cleaned_data['is_a_customer_payment_account']:
            if self.cleaned_data['account_type'] != "A":
                errors.append(_('A customer payment account must be an asset account'))
        if self.cleaned_data['is_product_inventory_activa']:
            if self.cleaned_data['account_type'] != "A":
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
                              'is_a_customer_payment_account')}),)
    save_as = True

    form = AccountForm
