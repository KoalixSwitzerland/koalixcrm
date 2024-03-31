# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _
from django import forms
from koalixcrm.accounting.models import Account
from koalixcrm.crm.documents.pdf_export import PDFExport
from koalixcrm.accounting.exceptions import AccountingPeriodNotFound
from koalixcrm.accounting.exceptions import TemplateSetMissingInAccountingPeriod
from koalixcrm.accounting.models import InlineBookings


class AccountingPeriod(models.Model):
    """Accounting period represents the equivalent of the business logic element of a fiscal year
    the accounting period is referred in the booking and is used as a supporting object to generate
    balance sheets and profit/loss statements"""
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name=_("Title"))  # For example "Year 2009", "1st Quarter 2009"
    begin = models.DateField(verbose_name=_("Begin"))
    end = models.DateField(verbose_name=_("End"))
    template_set_balance_sheet = models.ForeignKey("djangoUserExtension.DocumentTemplate",
                                                   on_delete=models.CASCADE,
                                                   verbose_name=_("Referred template for balance sheet"),
                                                   related_name='db_balancesheet_template_set',
                                                   null=True,
                                                   blank=True)
    template_profit_loss_statement = models.ForeignKey("djangoUserExtension.DocumentTemplate",
                                                       on_delete=models.CASCADE,
                                                       verbose_name=_("Referred template for profit, loss statement"),
                                                       related_name='db_profit_loss_statement_template_set',
                                                       null=True,
                                                       blank=True)

    def get_template_set(self, template_set):
        if template_set == self.template_set_balance_sheet:
            if self.template_set_balance_sheet:
                return self.template_set_balance_sheet
            else:
                raise TemplateSetMissingInAccountingPeriod((_("Template Set for balance sheet " +
                                                              "is missing in Accounting Period" + str(self))))
        elif template_set == self.template_profit_loss_statement:
            if self.template_profit_loss_statement:
                return self.template_profit_loss_statement
            else:
                raise TemplateSetMissingInAccountingPeriod((_("Template Set for profit loss statement" +
                                                              " is missing in Accounting Period" + str(self))))

    def get_fop_config_file(self, template_set):
        template_set = self.get_template_set(template_set)
        return template_set.get_fop_config_file()

    def get_xsl_file(self, template_set):
        template_set = self.get_template_set(template_set)
        return template_set.get_xsl_file()

    def create_pdf(self, template_set, printed_by):
        import koalixcrm.crm
        return koalixcrm.crm.documents.pdfexport.PDFExport.create_pdf(self, template_set, printed_by)

    def overall_earnings(self):
        earnings = 0
        accounts = Account.objects.all()
        for account in list(accounts):
            if account.account_type == "E":
                earnings += account.sum_of_all_bookings_within_accounting_period(self)
        return earnings

    def overall_spendings(self):
        spendings = 0
        accounts = Account.objects.all()
        for account in list(accounts):
            if account.account_type == "S":
                spendings += account.sum_of_all_bookings_within_accounting_period(self)
        return spendings

    def overall_assets(self):
        assets = 0
        accounts = Account.objects.all()
        for account in list(accounts):
            if account.account_type == "A":
                assets += account.sum_of_all_bookings_through_now(self)
        return assets

    def overall_liabilities(self):
        liabilities = 0
        accounts = Account.objects.all()
        for account in list(accounts):
            if account.account_type == "L":
                liabilities += account.sum_of_all_bookings_through_now(self)
        return liabilities

    def serialize_to_xml(self):
        objects = [self, ]
        main_xml = PDFExport.write_xml(objects)
        accounts = Account.objects.all()
        for account in accounts:
            account_xml = account.serialize_to_xml(self)
            main_xml = PDFExport.merge_xml(main_xml, account_xml)
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.accountingperiod']",
                                                       "Overall_Earnings",
                                                       self.overall_earnings())
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.accountingperiod']",
                                                       "Overall_Spendings",
                                                       self.overall_spendings())
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.accountingperiod']",
                                                       "Overall_Assets",
                                                       self.overall_assets())
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.accountingperiod']",
                                                       "Overall_Liabilities",
                                                       self.overall_liabilities())
        return main_xml

    @staticmethod
    def get_current_valid_accounting_period():
        """Returns the accounting period that is currently valid. Valid is an accounting_period when the current date
          lies between begin and end of the accounting_period

        Args:
          no arguments

        Returns:
          accounting_period (AccoutingPeriod)

        Raises:
          AccountingPeriodNotFound when there is no valid accounting Period"""
        current_valid_accounting_period = None
        for accounting_period in AccountingPeriod.objects.all():
            if accounting_period.begin < date.today() and accounting_period.end > date.today():
                return accounting_period
        if not current_valid_accounting_period:
            raise AccountingPeriodNotFound("The accounting period was not found")

    def get_all_prior_accounting_periods(self):
        """Returns the accounting period that is currently valid. Valid is an accountingPeriod when the current date
          lies between begin and end of the accountingPeriod

        Args:
          no arguments

        Returns:
          accounting_period (List of AccoutingPeriod)

        Raises:
          AccountingPeriodNotFound when there is no valid accounting Period"""
        accounting_periods = []
        for accounting_period in AccountingPeriod.objects.all():
            if accounting_period.end < self.begin:
                accounting_periods.append(accounting_period)
        if accounting_periods == []:
            raise AccountingPeriodNotFound("Accounting Period does not exist")
        return accounting_periods

    def __str__(self):
        return self.title

        # TODO: def createNewAccountingPeriod() Neues Geschäftsjahr erstellen

    class Meta:
        app_label = "accounting"
        verbose_name = _('Accounting Period')
        verbose_name_plural = _('Accounting Periods')


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
                                                obj.template_profit_loss_statement,)
            return response

    create_pdf_of_profit_loss_statement.short_description = _("Create PDF of Profit Loss Statement Sheet")

    actions = ['create_pdf_of_balance_sheet',
               'create_pdf_of_profit_loss_statement']
