# -*- coding: utf-8 -*-

from os import system
from const.accountTypeChoices import *
from crm.models import Contract
from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.db.models import signals
from xml.dom.minidom import Document
from middleware import threadlocals
from datetime import *

   
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
      #app_label_koalix = _("Accounting")
      verbose_name = _('Accounting Calculation Unit')
      verbose_name_plural = _('Accounting Calculation Units')
            
class Account(models.Model):
   accountNumber = models.IntegerField(verbose_name=_("Account Number"))
   title = models.CharField(verbose_name=_("Account Title"), max_length=50)
   accountType = models.CharField(verbose_name=_("Account Type"), max_length=1, choices=ACCOUNTTYPECHOICES)
   isopenreliabilitiesaccount = models.BooleanField(verbose_name=_("Is The Open Reliabilities Account"))
   # TODO: There may only be one isopenreliabilitiesaccount and it must be an activa
   isopeninterestaccount = models.BooleanField(verbose_name=_("Is The Open Interests Account"))
   # TODO: There may only be one openinterestaccount and it must be an activa
   isProductInventoryActiva = models.BooleanField(verbose_name=_("Is a Product Inventory Account"))
   # TODO: This can only be set when accountType is Activa and can not be customerpaymentaccount
   isACustomerPaymentAccount = models.BooleanField(verbose_name=_("Is a Customer Payment Account"))
   # TODO: This can only be set when accountType is Activa and can not be product inventry as well
   
   def value():
      sum = self.allBookings(fromAccount = False, accountingCalculationUnit = accountingCalculationUnit) - self.allBookings(fromAccount = True, accountingCalculationUnit = accountingCalculationUnit)
      if (self.accountType == 'P' or self.accountType == 'E'):
        sum = 0 - sum
      return sum
      
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
      #app_label_koalix = _("Accounting")
      verbose_name = _('Account')
      verbose_name_plural = _('Account')
      ordering = ['accountNumber']
      
class ProductCategorie(models.Model):
   title = models.CharField(verbose_name=_("Product Categorie Title"), max_length=50)
   profitAccount = models.ForeignKey(Account, verbose_name=_("Profit Account"), limit_choices_to="accountType=E", related_name="db_profit_account")
   lossAccount = models.ForeignKey(Account, verbose_name=_("Loss Account"),  limit_choices_to="accountType=S", related_name="db_loss_account")
   
   class Meta:
      app_label = "accounting"
      #app_label_koalix = _("Accounting")
      verbose_name = _('Product Categorie')
      verbose_name_plural = _('Product Categorie')

class Booking(models.Model):
   fromAccount = models.ForeignKey(Account, verbose_name=_("From Account"), related_name="db_booking_fromaccount")
   toAccount = models.ForeignKey(Account, verbose_name=_("To Account"), related_name="db_booking_toaccount")
   amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Amount"))
   description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
   bookingReference = models.ForeignKey('crm.Invoice', verbose_name=_("Booking Reference"), null=True, blank=True)
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
      #app_label_koalix = _("Accounting")
      verbose_name = _('Booking')
      verbose_name_plural = _('Bookings')

def postInitAutoUserHandler(sender, instance, **kwarg):
   instance.staff = threadlocals.get_current_user()
   instance.dateofcreation = date.today().__str__()

def preSaveAutoNowUserHandler(sender, instance, **kwarg):
   instance.lastmodifiedby = threadlocals.get_current_user()
   instance.lastmodification = date.today().__str__()
      
def preSaveCheckFlags(sender, instance, **kwarg):
   if (instance.isopenreliabilitiesaccount):
      openinterestaccounts = Account.objects.filter(isopenreliabilitiesaccount=True)
      if (instance.accountType != "P" ):
         instance.isopenreliabilitiesaccount = False
         #TODO: Correct Action when not Passiva
      elif openinterestaccounts:
         instance.isopenreliabilitiesaccount = False
         #TODO: Correct Action when there is already a isopenreliabilitiesaccount account
   if (instance.isopeninterestaccount):
      openinterestaccounts = Account.objects.filter(isopeninterestaccount=True)
      if (instance.accountType != "A" ):
         instance.isopeninterestaccount = False
         #TODO: Correct Action when not Activa
      elif openinterestaccounts:
         instance.isopeninterestaccount = False
         #TODO: Correct Action when there is already a isopenreliabilitiesaccount account
   if (instance.isACustomerPaymentAccount):
      if (instance.accountType != "A" ):
         instance.isACustomerPaymentAccount = False
         #TODO: Correct Action when not Activa
   if (instance.isProductInventoryActiva):
      if (instance.accountType != "A" ):
         instance.isProductInventoryActiva = False
         #TODO: Correct Action when not Activa
   
signals.post_init.connect(postInitAutoUserHandler, Booking)
signals.pre_save.connect(preSaveAutoNowUserHandler, Booking)
signals.pre_save.connect(preSaveCheckFlags, Account)