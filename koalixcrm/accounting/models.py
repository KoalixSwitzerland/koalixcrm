# -*- coding: utf-8 -*-

import os
from datetime import *
from subprocess import check_output
from subprocess import STDOUT
from xml.dom.minidom import Document

from django.conf import settings
from django.core import serializers
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm import djangoUserExtension
from koalixcrm.crm.exceptions import UserExtensionMissing
from koalixcrm.accounting.const.accountTypeChoices import *
from koalixcrm.accounting.exceptions import NoObjectsToBeSerialzed
from koalixcrm.accounting.exceptions import ProgrammingError
from koalixcrm.accounting.exceptions import AccountingPeriodNotFound


class AccountingPeriod(models.Model):
    """Accounting period represents the equivalent of the business logic element of a fiscal year
    the accounting period is referred in the booking and is used as a supporting object to generate
    balance sheets and profit/loss statements"""
    title = models.CharField(max_length=200, verbose_name=_("Title"))  # For example "Year 2009", "1st Quarter 2009"
    begin = models.DateField(verbose_name=_("Begin"))
    end = models.DateField(verbose_name=_("End"))
    template_set = models.ForeignKey("djangoUserExtension.DocumentTemplate", verbose_name=_("Referred Template"), null=True,
                                     blank=True)

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
            raise AccountingPeriodNotFound()
        return accounting_periods

    @staticmethod
    def createXML(whatToCreate):
        """This method serialize requestd objects into a XML file which is located in the PDF_OUTPUT_ROOT folder.

          Args:
            whatToCreate (str): Which objects that have to be serialized

          Returns:
            path_full to the location of the file

          Raises:
            ProgrammingError will be raised when incorrect objects to be serialized was selected
            NoObjectToBeSerialized will be raised when no object can be serialized"""

        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        if whatToCreate == "allAccount":
            path_fullToOutputFile = os.path.join(settings.PDF_OUTPUT_ROOT, "accounts.xml")
            objectsToSerialize = Account.objects.all()
        else:
            raise ProgrammingError(
                _("During XML Export it was not correctly specified which data that has to be exported"))
        out = open(os.path.join(settings.PDF_OUTPUT_ROOT, "accounts.xml"), "w")
        if objectsToSerialize == '':
            raise NoObjectsToBeSerialzed(_("During XML Export it was not correctly specied data has to be exported"))
        else:
            xml_serializer.serialize(objectsToSerialize, stream=out, indent=3)
        out.close()
        return path_fullToOutputFile

        # TODO  def importAllAccountsXML(self):

    def createPDF(self, raisedbyuser, whatToCreate):
        userExtension = djangoUserExtension.models.UserExtension.objects.filter(user=raisedbyuser.id)
        if (len(userExtension) == 0):
            raise UserExtensionMissing(_("During BalanceSheet PDF Export"))
        doc = Document()
        if whatToCreate == "balanceSheet":
            main = doc.createElement("koalixaccountingbalacesheet")
            out = open(os.path.join(settings.PDF_OUTPUT_ROOT, "balancesheet_" + str(self.id) + ".xml"), "wb")
        else:
            main = doc.createElement("koalixaccountingprofitlossstatement")
            out = open(os.path.join(settings.PDF_OUTPUT_ROOT, "profitlossstatement_" + str(self.id) + ".xml"), "wb")
        accountingPeriodName = doc.createElement("accountingPeriodName")
        accountingPeriodName.appendChild(doc.createTextNode(self.__str__()))
        main.appendChild(accountingPeriodName)
        organisiationname = doc.createElement("organisiationname")
        organisiationname.appendChild(doc.createTextNode(userExtension[0].defaultTemplateSet.organisationname))
        main.appendChild(organisiationname)
        accountingPeriodTo = doc.createElement("accountingPeriodTo")
        accountingPeriodTo.appendChild(doc.createTextNode(self.end.year.__str__()))
        main.appendChild(accountingPeriodTo)
        accountingPeriodFrom = doc.createElement("accountingPeriodFrom")
        accountingPeriodFrom.appendChild(doc.createTextNode(self.begin.year.__str__()))
        main.appendChild(accountingPeriodFrom)
        headerPicture = doc.createElement("headerpicture")
        headerPicture.appendChild(doc.createTextNode(userExtension[0].defaultTemplateSet.logo.path_full))
        main.appendChild(headerPicture)
        accounts = Account.objects.all()
        overallValueBalance = 0
        overallValueProfitLoss = 0
        for account in list(accounts):
            withinAccountingPeriod = account.sum_of_all_bookings_within_accounting_period(self)
            beforeAccountingPeriod = account.sum_of_all_bookings_before_accounting_period(self)
            currentValue = withinAccountingPeriod + beforeAccountingPeriod
            if (currentValue != 0):
                currentAccountElement = doc.createElement("Account")
                accountNumber = doc.createElement("AccountNumber")
                accountNumber.appendChild(doc.createTextNode(account.accountNumber.__str__()))
                beforeAccountingPeriodAccountElement = doc.createElement("beforeAccountingPeriod")
                beforeAccountingPeriodAccountElement.appendChild(doc.createTextNode(beforeAccountingPeriod.__str__()))
                currentValueElement = doc.createElement("currentValue")
                currentValueElement.appendChild(doc.createTextNode(currentValue.__str__()))
                accountNameElement = doc.createElement("accountName")
                accountNameElement.appendChild(doc.createTextNode(account.title))
                currentAccountElement.setAttribute("accountType", account.accountType.__str__())
                currentAccountElement.appendChild(accountNumber)
                currentAccountElement.appendChild(accountNameElement)
                currentAccountElement.appendChild(currentValueElement)
                currentAccountElement.appendChild(beforeAccountingPeriodAccountElement)
                main.appendChild(currentAccountElement)
                if account.accountType == "A":
                    overallValueBalance = overallValueBalance + currentValue;
                if account.accountType == "L":
                    overallValueBalance = overallValueBalance - currentValue;
                if account.accountType == "E":
                    overallValueProfitLoss = overallValueProfitLoss + currentValue;
                if account.accountType == "S":
                    overallValueProfitLoss = overallValueProfitLoss - currentValue;
        totalProfitLoss = doc.createElement("TotalProfitLoss")
        totalProfitLoss.appendChild(doc.createTextNode(overallValueProfitLoss.__str__()))
        main.appendChild(totalProfitLoss)
        totalBalance = doc.createElement("TotalBalance")
        totalBalance.appendChild(doc.createTextNode(overallValueBalance.__str__()))
        main.appendChild(totalBalance)
        doc.appendChild(main)
        out.write(doc.toprettyxml(indent=" ", newl="\n", encoding="utf-8"))
        out.close()
        if whatToCreate == "balanceSheet":
            check_output(
                [settings.FOP_EXECUTABLE, '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path_full, '-xml',
                 os.path.join(settings.PDF_OUTPUT_ROOT, 'balancesheet_' + str(self.id) + '.xml'), '-xsl',
                 userExtension[0].defaultTemplateSet.balancesheetXSLFile.xslfile.path_full, '-pdf',
                 os.path.join(settings.PDF_OUTPUT_ROOT, 'balancesheet_' + str(self.id) + '.pdf')], stderr=STDOUT)
            return os.path.join(settings.PDF_OUTPUT_ROOT, "balancesheet_" + str(self.id) + ".pdf")
        else:
            check_output(
                [settings.FOP_EXECUTABLE, '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path_full, '-xml',
                 os.path.join(settings.PDF_OUTPUT_ROOT, 'profitlossstatement_' + str(self.id) + '.xml'), '-xsl',
                 userExtension[0].defaultTemplateSet.profitLossStatementXSLFile.xslfile.path_full, '-pdf',
                 os.path.join(settings.PDF_OUTPUT_ROOT, 'profitlossstatement_' + str(self.id) + '.pdf')], stderr=STDOUT)
            return os.path.join(settings.PDF_OUTPUT_ROOT, "profitlossstatement_" + str(self.id) + ".pdf")

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
        if self.accountType == 'E' or self.accountType == 'L':
            calculated_sum = -calculated_sum
        return calculated_sum

    def sum_of_all_bookings_before_accounting_period(self, current_accounting_period):
        accounting_periods = AccountingPeriod.get_all_prior_accounting_periods(current_accounting_period)
        sum = 0
        for accounting_period in accounting_periods:
            sum += self.all_bookings_within_accounting_period(from_account=False,
                                                              accounting_period=accounting_period) - self.all_bookings_within_accounting_period(
                from_account=True, accounting_period=accounting_period)
        if self.account_type == 'E' or self.account_type == 'L':
            sum = -sum
        return sum

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
