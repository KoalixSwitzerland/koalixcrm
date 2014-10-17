# -*- coding: utf-8 -*-

from subprocess import *
from xml.dom.minidom import Document
from datetime import *
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from const.accountTypeChoices import *
from crm_core.models import UserExtension


class AccountingPeriod(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))  # For example "Year 2009", "1st Quarter 2009"
    begin = models.DateField(verbose_name=_("Begin"))
    end = models.DateField(verbose_name=_("End"))

    @staticmethod
    def get_current_valid_accounting_period():
        """Returns the accounting period that is currently valid. Valid is an accountingPeriod when the current date
           lies between begin and end of the accountingPeriod

        Args:
          no arguments

        Returns:
          accoutingPeriod (AccoutingPeriod)

        Raises:
          NoFeasableAccountingPeriodFound when there is no valid accounting Period"""
        current_valid_accounting_period = None

        for accounting_period in AccountingPeriod.objects.all():
            if accounting_period.begin < date.today() < accounting_period.end:
                return accounting_period

        if current_valid_accounting_period is None:
            raise Exception('No accounting period found')

    def create_pdf(self, raised_by_user, what_to_create):
        user_extension = UserExtension.objects.filter(user=raised_by_user.id)
        doc = Document()

        if len(user_extension) == 0:
            raise Exception(_("During BalanceSheet PDF Export"))

        if what_to_create == "balanceSheet":
            main = doc.createElement("koalixaccountingbalacesheet")
            out = open(settings.PDF_OUTPUT_ROOT + "balancesheet_" + str(self.id) + ".xml", "w")
        else:
            main = doc.createElement("koalixaccountingprofitlossstatement")
            out = open(settings.PDF_OUTPUT_ROOT + "profitlossstatement_" + str(self.id) + ".xml", "w")

        accounting_period_name = doc.createElement("accountingPeriodName")
        accounting_period_name.appendChild(doc.createTextNode(self.__unicode__()))
        main.appendChild(accounting_period_name)
        organisation_name = doc.createElement("organisiationname")
        organisation_name.appendChild(
            doc.createTextNode(settings.MEDIA_ROOT + user_extension[0].defaultTemplateSet.organisationname))
        main.appendChild(organisation_name)
        accounting_period_to = doc.createElement("accountingPeriodTo")
        accounting_period_to.appendChild(doc.createTextNode(self.end.year.__str__()))
        main.appendChild(accounting_period_to)
        accounting_period_from = doc.createElement("accountingPeriodFrom")
        accounting_period_from.appendChild(doc.createTextNode(self.begin.year.__str__()))
        main.appendChild(accounting_period_from)
        header_picture = doc.createElement("headerpicture")
        header_picture.appendChild(
            doc.createTextNode(settings.MEDIA_ROOT + user_extension[0].defaultTemplateSet.logo.path))
        main.appendChild(header_picture)
        account_number = doc.createElement("AccountNumber")
        accounts = Account.objects.all()
        overall_value_balance = 0
        overall_value_profit_loss = 0

        for account in list(accounts):
            current_value = account.value_now(self)

            if current_value != 0:
                current_account_element = doc.createElement("Account")
                account_number = doc.createElement("AccountNumber")
                account_number.appendChild(doc.createTextNode(account.accountNumber.__str__()))
                current_value_element = doc.createElement("currentValue")
                current_value_element.appendChild(doc.createTextNode(current_value.__str__()))
                account_name_element = doc.createElement("accountName")
                account_name_element.appendChild(doc.createTextNode(account.title))
                current_account_element.setAttribute("accountType", account.accountType.__str__())
                current_account_element.appendChild(account_number)
                current_account_element.appendChild(account_name_element)
                current_account_element.appendChild(current_value_element)
                main.appendChild(current_account_element)

                if account.accountType == "A":
                    overall_value_balance = overall_value_balance + current_value

                if account.accountType == "L":
                    overall_value_balance = overall_value_balance - current_value

                if account.accountType == "E":
                    overall_value_profit_loss = overall_value_profit_loss + current_value

                if account.accountType == "S":
                    overall_value_profit_loss = overall_value_profit_loss - current_value

        total_profit_loss = doc.createElement("TotalProfitLoss")
        total_profit_loss.appendChild(doc.createTextNode(overall_value_profit_loss.__str__()))
        main.appendChild(total_profit_loss)
        total_balance = doc.createElement("TotalBalance")
        total_balance.appendChild(doc.createTextNode(overall_value_balance.__str__()))
        main.appendChild(total_balance)
        doc.appendChild(main)
        out.write(doc.toxml("utf-8"))
        out.close()

        if what_to_create == "balanceSheet":
            check_output(['/usr/bin/fop', '-c', user_extension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml',
                          settings.PDF_OUTPUT_ROOT + 'balancesheet_' + str(self.id) + '.xml', '-xsl',
                          user_extension[0].defaultTemplateSet.balancesheetXSLFile.xslfile.path, '-pdf',
                          settings.PDF_OUTPUT_ROOT + 'balancesheet_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "balancesheet_" + str(self.id) + ".pdf"
        else:
            check_output(['/usr/bin/fop', '-c', user_extension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml',
                          settings.PDF_OUTPUT_ROOT + 'profitlossstatement_' + str(self.id) + '.xml', '-xsl',
                          user_extension[0].defaultTemplateSet.profitLossStatementXSLFile.xslfile.path, '-pdf',
                          settings.PDF_OUTPUT_ROOT + 'profitlossstatement_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "profitlossstatement_" + str(self.id) + ".pdf"

    def __unicode__(self):
        return self.title

    # TODO: def createNewAccountingPeriod() Neues Geschäftsjahr erstellen

    class Meta:
        verbose_name = _('Accounting Period')
        verbose_name_plural = _('Accounting Periods')


class Account(models.Model):
    accountNumber = models.IntegerField(verbose_name=_("Account Number"))
    title = models.CharField(verbose_name=_("Account Title"), max_length=50)
    accountType = models.CharField(verbose_name=_("Account Type"), max_length=1, choices=ACCOUNTTYPECHOICES)
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    originalAmount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Original Amount"),
                                         default=0.00)
    isopenreliabilitiesaccount = models.BooleanField(verbose_name=_("Is The Open Liabilities Account"),
                                                     default=False)
    isopeninterestaccount = models.BooleanField(verbose_name=_("Is The Open Interests Account"), default=False)
    isProductInventoryActiva = models.BooleanField(verbose_name=_("Is a Product Inventory Account"), default=False)
    isACustomerPaymentAccount = models.BooleanField(verbose_name=_("Is a Customer Payment Account"), default=False)

    def value(self):
        booking_sum = self.all_bookings(from_account=False) - self.all_bookings(from_account=True)

        if self.accountType == 'P' or self.accountType == 'E':
            booking_sum = 0 - booking_sum
        return booking_sum

    def value_now(self, accounting_period):
        bookings_sum = self.all_bookings_in_accounting_period(
            from_account=False, accounting_period=accounting_period) - self.all_bookings_in_accounting_period(
            from_account=True, accounting_period=accounting_period)
        return bookings_sum

    def all_bookings(self, from_account):
        bookings_sum = 0
        if from_account:
            bookings = Booking.objects.filter(fromAccount=self.id)
        else:
            bookings = Booking.objects.filter(toAccount=self.id)

        for booking in list(bookings):
            bookings_sum = bookings_sum + booking.amount

        return bookings_sum

    def all_bookings_in_accounting_period(self, from_account, accounting_period):
        bookings_sum = 0
        if from_account:
            bookings = Booking.objects.filter(fromAccount=self.id, accountingPeriod=accounting_period.id)
        else:
            bookings = Booking.objects.filter(toAccount=self.id, accountingPeriod=accounting_period.id)

        for booking in list(bookings):
            bookings_sum = bookings_sum + booking.amount

        return bookings_sum

    def __unicode__(self):
        return self.accountNumber.__str__() + " " + self.title

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Account')
        ordering = ['accountNumber']


class ProductCategory(models.Model):
    title = models.CharField(verbose_name=_("Product Categorie Title"), max_length=50)
    profitAccount = models.ForeignKey(Account, verbose_name=_("Profit Account"),
                                      limit_choices_to={"accountType": "E"},
                                      related_name="db_profit_account")
    lossAccount = models.ForeignKey(Account, verbose_name=_("Loss Account"), limit_choices_to={"accountType": "S"},
                                    related_name="db_loss_account")

    class Meta:
        verbose_name = _('Product Categorie')
        verbose_name_plural = _('Product Categories')

    def __unicode__(self):
        return self.title


class Booking(models.Model):
    fromAccount = models.ForeignKey(Account, verbose_name=_("From Account"), related_name="db_booking_fromaccount")
    toAccount = models.ForeignKey(Account, verbose_name=_("To Account"), related_name="db_booking_toaccount")
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Amount"))
    description = models.CharField(verbose_name=_("Description"), max_length=120, null=True, blank=True)
    bookingReference = models.ForeignKey('crm_core.Invoice', verbose_name=_("Booking Reference"), null=True, blank=True)
    bookingDate = models.DateTimeField(verbose_name=_("Booking at"))
    accountingPeriod = models.ForeignKey(AccountingPeriod, verbose_name=_("AccountingPeriod"))
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                              verbose_name=_("Reference Staff"), related_name="db_booking_refstaff")
    dateOfCreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastModification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastModifiedBy = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                                       verbose_name=_("Last modified by"), related_name="db_booking_lstmodified")

    def __unicode__(self):
        return self.fromAccount.__str__() + " " + self.toAccount.__str__() + " " + self.amount.__str__()

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')