# -*- coding: utf-8 -*-
from datetime import *

from django.db import models
from django.utils.translation import ugettext as _
from rest_framework import serializers

from koalixcrm.accounting.const.accountTypeChoices import *
from koalixcrm.accounting.exceptions import AccountingPeriodNotFound
from koalixcrm.accounting.exceptions import TemplateSetMissingInAccountingPeriod
from koalixcrm.crm.documents.pdfexport import PDFExport


class AccountingPeriod(models.Model):
    """Accounting period represents the equivalent of the business logic element of a fiscal year
    the accounting period is referred in the booking and is used as a supporting object to generate
    balance sheets and profit/loss statements"""
    title = models.CharField(max_length=200, verbose_name=_("Title"))  # For example "Year 2009", "1st Quarter 2009"
    begin = models.DateField(verbose_name=_("Begin"))
    end = models.DateField(verbose_name=_("End"))
    template_set_balance_sheet = models.ForeignKey("djangoUserExtension.DocumentTemplate",
                                                   verbose_name=_("Referred template for balance sheet"),
                                                   related_name='db_balancesheet_template_set',
                                                   null=True,
                                                   blank=True)
    template_profit_loss_statement = models.ForeignKey("djangoUserExtension.DocumentTemplate",
                                                       verbose_name=_("Referred template for profit, loss statement"),
                                                       related_name='db_profit_loss_statement_template_set',
                                                       null=True,
                                                       blank=True)

    def get_template_set(self, template_set):
        if template_set == self.template_set_balance_sheet:
            if self.template_set_balance_sheet:
                return self.template_set_balance_sheet
            else:
                raise TemplateSetMissingInAccountingPeriod(
                    (_("Template Set for balance sheet is missing in Accounting Period" + str(self))))
        elif template_set == self.template_profit_loss_statement:
            if self.template_profit_loss_statement:
                return self.template_profit_loss_statement
            else:
                raise TemplateSetMissingInAccountingPeriod(
                    (_("Template Set for profit loss statement is missing in Accounting Period" + str(self))))

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
        earnings = 0;
        accounts = Account.objects.all()
        for account in list(accounts):
            if account.account_type == "E":
                earnings += account.sum_of_all_bookings_within_accounting_period(self)
        return earnings

    def overall_spendings(self):
        spendings = 0;
        accounts = Account.objects.all()
        for account in list(accounts):
            if account.account_type == "S":
                spendings += account.sum_of_all_bookings_within_accounting_period(self)
        return spendings

    def overall_assets(self):
        assets = 0;
        accounts = Account.objects.all()
        for account in list(accounts):
            if account.account_type == "A":
                assets += account.sum_of_all_bookings_through_now(self)
        return assets

    def overall_liabilities(self):
        liabilities = 0;
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
            raise AccountingPeriodNotFound()

    @staticmethod
    def get_all_prior_accounting_periods(target_accounting_period):
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
            if accounting_period.end < target_accounting_period.begin:
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


class Account(models.Model):
    account_number = models.IntegerField(verbose_name=_("Account Number"))
    title = models.CharField(verbose_name=_("Account Title"), max_length=50)
    account_type = models.CharField(verbose_name=_("Account Type"), max_length=1, choices=ACCOUNTTYPECHOICES)
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

    sum_of_all_bookings.short_description = _("Value");

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
            accounting_periods = AccountingPeriod.get_all_prior_accounting_periods(current_accounting_period)
        except AccountingPeriodNotFound as e:
            return 0;
        sum = 0
        for accounting_period in accounting_periods:
            sum += self.all_bookings_within_accounting_period(from_account=False,
                                                              accounting_period=accounting_period) - self.all_bookings_within_accounting_period(
                from_account=True, accounting_period=accounting_period)
        if self.account_type == 'E' or self.account_type == 'L':
            sum = -sum
        return sum

    def sum_of_all_bookings_through_now(self, current_accounting_period):
        within_accounting_period = self.sum_of_all_bookings_within_accounting_period(current_accounting_period)
        before_accounting_period = self.sum_of_all_bookings_before_accounting_period(current_accounting_period)
        current_value = within_accounting_period + before_accounting_period
        return current_value

    def all_bookings(self, from_account):
        sum = 0
        if from_account:
            bookings = Booking.objects.filter(from_account=self.id)
        else:
            bookings = Booking.objects.filter(to_account=self.id)

        for booking in list(bookings):
            sum += booking.amount

        return sum

    def all_bookings_within_accounting_period(self, from_account, accounting_period):
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
                                                       self.sum_of_all_bookings_within_accounting_period(
                                                           accounting_period))
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.account']",
                                                       "sum_of_all_bookings_through_now",
                                                       self.sum_of_all_bookings_through_now(accounting_period))
        main_xml = PDFExport.append_element_to_pattern(main_xml,
                                                       "object/[@model='accounting.account']",
                                                       "sum_of_all_bookings_before_accounting_period",
                                                       self.sum_of_all_bookings_before_accounting_period(
                                                           accounting_period))
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


class ProductCategorie(models.Model):
    title = models.CharField(verbose_name=_("Product Categorie Title"), max_length=50)
    profit_account = models.ForeignKey(Account, verbose_name=_("Profit Account"), limit_choices_to={"accountType": "E"},
                                       related_name="db_profit_account")
    loss_account = models.ForeignKey(Account, verbose_name=_("Loss Account"), limit_choices_to={"accountType": "S"},
                                     related_name="db_loss_account")

    class Meta:
        app_label = "accounting"
        verbose_name = _('Product Categorie')
        verbose_name_plural = _('Product Categories')

    def __str__(self):
        return self.title


class Booking(models.Model):
    from_account = models.ForeignKey(Account, verbose_name=_("From Account"), related_name="db_booking_fromaccount")
    to_account = models.ForeignKey(Account, verbose_name=_("To Account"), related_name="db_booking_toaccount")
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Amount"))
    description = models.CharField(verbose_name=_("Description"), max_length=120, null=True, blank=True)
    booking_reference = models.ForeignKey('crm.Invoice', verbose_name=_("Booking Reference"), null=True, blank=True)
    booking_date = models.DateTimeField(verbose_name=_("Booking at"))
    accounting_period = models.ForeignKey(AccountingPeriod, verbose_name=_("AccountingPeriod"))
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                              verbose_name=_("Reference Staff"), related_name="db_booking_refstaff")
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    last_modified_by = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                                         verbose_name=_("Last modified by"), related_name="db_booking_lstmodified")

    def booking_date_only(self):
        return self.booking_date.date()

    booking_date_only.short_description = _("Date");

    def __str__(self):
        return self.from_account.__str__() + " " + self.to_account.__str__() + " " + self.amount.__str__()

    class Meta:
        app_label = "accounting"
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')


class AccountMinimalJSONSerializer(serializers.HyperlinkedModelSerializer):
    accountNumber = serializers.IntegerField(source='account_number')

    class Meta:
        model = Account
        fields = ('id',
                  'accountNumber',
                  'title')


class AccountJSONSerializer(serializers.HyperlinkedModelSerializer):
    accountNumber = serializers.IntegerField(source='account_number', allow_null=False)
    accountType = serializers.CharField(source='account_type', allow_null=False)
    isOpenReliabilitiesAccount = serializers.BooleanField(source='is_open_reliabilities_account')
    isOpenInterestAccount = serializers.BooleanField(source='is_open_interest_account')
    isProductInventoryActiva = serializers.BooleanField(source='is_product_inventory_activa')
    isCustomerPaymentAccount = serializers.BooleanField(source='is_a_customer_payment_account')

    class Meta:
        model = Account
        fields = ('id',
                  'accountNumber',
                  'title',
                  'accountType',
                  'description',
                  'isOpenReliabilitiesAccount',
                  'isOpenInterestAccount',
                  'isProductInventoryActiva',
                  'isCustomerPaymentAccount')
        depth = 1


class ProductCategoryJSONSerializer(serializers.HyperlinkedModelSerializer):
    profitAccount = AccountMinimalJSONSerializer(source='profit_account')
    lossAccount = AccountMinimalJSONSerializer(source='loss_account')

    class Meta:
        model = ProductCategorie
        fields = ('id',
                  'title',
                  'profitAccount',
                  'lossAccount')
        depth = 1

    def create(self, validated_data):
        product_category = ProductCategorie()
        product_category.title = validated_data['title']

        # Deserialize profit account
        profit_account = validated_data.pop('profit_account')
        if profit_account:
            if profit_account.get('id', None):
                product_category.profit_account = Account.objects.get(id=profit_account.get('id', None))
            else:
                product_category.profit_account = None

        # Deserialize loss account
        loss_account = validated_data.pop('loss_account')
        if loss_account:
            if loss_account.get('id', None):
                product_category.loss_account = Account.objects.get(id=loss_account.get('id', None))
            else:
                product_category.loss_account = None

        product_category.save()
        return product_category

    def update(self, instance, validated_data):
        instance.title = validated_data.get('description', instance.description)

        # Deserialize profit account
        profit_account = validated_data.pop('profit_account')
        if profit_account:
            if profit_account.get('id', instance.profit_account_id):
                instance.profit_account = Account.objects.get(id=profit_account.get('id', None))
            else:
                instance.profit_account = instance.profit_account_id
        else:
            instance.profit_account = None

        # Deserialize loss account
        loss_account = validated_data.pop('loss_account')
        if loss_account:
            if loss_account.get('id', instance.loss_account_id):
                instance.loss_account = Account.objects.get(id=loss_account.get('id', None))
            else:
                instance.loss_account = instance.loss_account_id
        else:
            instance.loss_account = None

        instance.save()
        return instance
