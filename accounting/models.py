# -*- coding: utf-8 -*-

from django.db import models
from const.accountTypeChoices import *
from crm.models import Contract
from django.utils.translation import ugettext as _
from os import system
from xml.dom.minidom import Document

   
class AccountingCalculationUnit(models.Model):
   title =  models.CharField(max_length=200, verbose_name=_("Title")) # For example "Year 2009", "1st Quarter 2009"
   begin = models.DateField(verbose_name=_("Begin"))
   end = models.DateField(verbose_name=_("End"))
            
   def createBalanceSheetPDF(self):
      out = open("/tmp/balancesheet_"+str(self.id)+".xml","w")
      doc = Document()
      main = doc.createElement("koalixaccountingbalacesheet")
      calculationUnitName = doc.createElement("calculationUnitName")
      calculationUnitName.appendChild(doc.createTextNode(self.__unicode__()))
      main.appendChild(calculationUnitName)
      calculationUnitTo = doc.createElement("calculationUnitTo")
      calculationUnitTo.appendChild(doc.createTextNode(self.end.year.__str__()))
      main.appendChild(calculationUnitTo)
      calculationUnitFrom = doc.createElement("calculationUnitFrom")
      calculationUnitFrom.appendChild(doc.createTextNode(self.begin.year.__str__()))
      main.appendChild(calculationUnitFrom)
      accountNumber = doc.createElement("AccountNumber")
      accounts = Account.objects.all()
      for account in list(accounts) :
         currentValue = account.valueNow(self)
         if (currentValue != 0):
            currentAccountElement = doc.createElement("Account")
            accountNumber = doc.createElement("AccountNumber")
            accountNumber.appendChild(doc.createTextNode(account.accountNumber.__str__()))
            currentValueElement = doc.createElement("currentValue")
            currentValueElement.appendChild(doc.createTextNode(currentValue.__str__()))
            accountNameElement = doc.createElement("accountName")
            accountNameElement.appendChild(doc.createTextNode(account.title))
            currentAccountElement.setAttribute("accountType", account.accountType.__str__())
            currentAccountElement.appendChild(accountNumber)
            currentAccountElement.appendChild(accountNameElement)
            currentAccountElement.appendChild(currentValueElement)
            main.appendChild(currentAccountElement)
      doc.appendChild(main)
      out.write(doc.toprettyxml(indent="  "))
      system("fop -c /var/www/koalixcrm/verasans.xml -xml /tmp/balancesheet_"+str(self.id)+".xml -xsl /var/www/koalixcrm/balancesheet.xsl -pdf /tmp/balancesheet_"+str(self.id)+".pdf")
      return "/tmp/balancesheet_"+str(self.id)+".pdf"
      
   def __unicode__(self):
      return  self.title
     
# TODO: def createProfitAndLossStatementPDF() Erfolgsrechnung

# TODO: def createNewCalculationUnit() Neues Geschäftsjahr erstellen
   
   class Meta:
      app_label = "accounting"
      verbose_name = _('Accounting Calculation Unit')
      verbose_name_plural = _('Accounting Calculation Units')
           
class Account(models.Model):
   accountNumber = models.IntegerField(verbose_name=_("Account Number"))
   title = models.CharField(verbose_name=_("Account Title"), max_length=50)
   accountType = models.CharField(verbose_name=_("Account Type"), max_length=1, choices=ACCOUNTTYPECHOICES)
   
   
   def valueNow(self, accountingCalculationUnit):
      sum = self.allBookings(fromAccount = False, accountingCalculationUnit = accountingCalculationUnit) - self.allBookings(fromAccount = True, accountingCalculationUnit = accountingCalculationUnit)
      return sum

   def allBookings(self, fromAccount, accountingCalculationUnit):
      sum = 0
      if (fromAccount == True):
         bookings = Booking.objects.filter(fromAccount=self.id, accountingCalculationUnit=accountingCalculationUnit.id)
      else:
         bookings = Booking.objects.filter(toAccount=self.id, accountingCalculationUnit=accountingCalculationUnit.id)
      
      for booking in list(bookings):
         sum = sum + booking.amount
         
      return sum
      
   def __unicode__(self):
      return  self.accountNumber.__str__()  + " " + self.title
      
   class Meta:
      app_label = "accounting"
      verbose_name = _('Account')
      verbose_name_plural = _('Account')
      ordering = ['accountNumber']

class Booking(models.Model):
   fromAccount = models.ForeignKey(Account, verbose_name=_("From Account"), related_name="db_booking_fromaccount")
   toAccount = models.ForeignKey(Account, verbose_name=_("To Account"), related_name="db_booking_toaccount")
   amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Amount"))
   description = models.TextField(verbose_name=_("Description"), blank=True)
   bookingReference = models.ForeignKey(Contract, null=True, blank=True)
   bookingDate = models.DateTimeField(verbose_name = _("Booking at"))
   accountingCalculationUnit = models.ForeignKey(AccountingCalculationUnit, verbose_name=_("AccountingCalculationUnit"))
   staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Reference Staff"), related_name="db_booking_refstaff")
   dateofcreation = models.DateTimeField(auto_now_add=True, verbose_name = _("Created at"))
   lastmodification = models.DateTimeField(auto_now=True, verbose_name = _("Last modified"), null=True, blank=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Last modified by"), related_name="db_booking_lstmodified")
   
   def __unicode__(self):
      return  self.fromAccount.__str__()  + " " + self.toAccount.__str__()  + " " + self.amount.__str__() 
      
   class Meta:
      app_label = "accounting"
      verbose_name = _('Booking')
      verbose_name_plural = _('Bookings')
