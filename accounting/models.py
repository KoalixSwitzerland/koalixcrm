# -*- coding: utf-8 -*-

from subprocess import *
from const.accountTypeChoices import *
from crm.models import Contract
from crm.exceptions import TemplateSetMissing
from crm.exceptions import UserExtensionMissing
from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.db.models import signals
from xml.dom.minidom import Document
from datetime import *
import settings
import djangoUserExtension

   
class AccountingPeriod(models.Model):
  title =  models.CharField(max_length=200, verbose_name=_("Title")) # For example "Year 2009", "1st Quarter 2009"
  begin = models.DateField(verbose_name=_("Begin"))
  end = models.DateField(verbose_name=_("End"))
  
  @staticmethod
  def getCurrentValidAccountingPeriod():
     currentValidAccountingPeriod = None
     for accountingPeriod in AccountingPeriod.objects.all():
       if accountingPeriod.begin < date.today() and accountingPeriod.end > date.today():
         return accountingPeriod
     if currentValidAccountingPeriod == None:
       raise NoFeasableAccountingPeriodFound()
  
  def createBalanceSheetPDF(self, raisedbyuser):
    userExtension = djangoUserExtension.models.UserExtension.objects.filter(user=raisedbyuser.id)
    if (len(userExtension) == 0):
      raise UserExtensionMissing(_("During BalanceSheet PDF Export"))
    out = open(settings.PDF_OUTPUT_ROOT+"balancesheet_"+str(self.id)+".xml", "w")
    doc = Document()
    main = doc.createElement("koalixaccountingbalacesheet")
    accountingPeriodName = doc.createElement("accountingPeriodName")
    accountingPeriodName.appendChild(doc.createTextNode(self.__unicode__()))
    main.appendChild(accountingPeriodName)
    organisiationname = doc.createElement("organisiationname")
    organisiationname.appendChild(doc.createTextNode(settings.MEDIA_ROOT+userExtension[0].defaultTemplateSet.organisationname))
    main.appendChild(organisiationname)
    accountingPeriodTo = doc.createElement("accountingPeriodTo")
    accountingPeriodTo.appendChild(doc.createTextNode(self.end.year.__str__()))
    main.appendChild(accountingPeriodTo)
    accountingPeriodFrom = doc.createElement("accountingPeriodFrom")
    accountingPeriodFrom.appendChild(doc.createTextNode(self.begin.year.__str__()))
    main.appendChild(accountingPeriodFrom)
    headerPicture = doc.createElement("headerpicture")
    headerPicture.appendChild(doc.createTextNode(settings.MEDIA_ROOT+userExtension[0].defaultTemplateSet.logo.path))
    main.appendChild(headerPicture)
    accountNumber = doc.createElement("AccountNumber")
    accounts = Account.objects.all()
    overallvalue = 0
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
          if account.accountType == "A":
            overallvalue = overallvalue + currentValue;
          if account.accountType == "L":
            overallvalue = overallvalue - currentValue;
    profitloss = doc.createElement("ProfitLoss")
    profitloss.appendChild(doc.createTextNode(overallvalue.__str__()))
    main.appendChild(profitloss)
    doc.appendChild(main)
    out.write(doc.toxml("utf-8"))
    out.close()
    log = open(settings.PDF_OUTPUT_ROOT+"log.txt", "w")
    check_output(['/usr/bin/fop', '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml', settings.PDF_OUTPUT_ROOT+'balancesheet_'+str(self.id)+'.xml', '-xsl', userExtension[0].defaultTemplateSet.balancesheetXSLFile.xslfile.path, '-pdf', settings.PDF_OUTPUT_ROOT+'balancesheet_'+str(self.id)+'.pdf'], stderr=STDOUT)
    return settings.PDF_OUTPUT_ROOT+"balancesheet_"+str(self.id)+".pdf"  
    
  def createProfitLossStatementPDF(self, raisedbyuser):
    userExtension = djangoUserExtension.models.UserExtension.objects.filter(user=raisedbyuser.id)
    if (len(userExtension) == 0):
      raise UserExtensionMissing(_("During BalanceSheet PDF Export"))
    out = open(settings.PDF_OUTPUT_ROOT+"profitlossstatement_"+str(self.id)+".xml", "w")
    doc = Document()
    main = doc.createElement("koalixaccountingprofitlossstatement")
    accountingPeriodName = doc.createElement("accountingPeriodName")
    accountingPeriodName.appendChild(doc.createTextNode(self.__unicode__()))
    main.appendChild(accountingPeriodName)
    organisationname = doc.createElement("organisiationname")
    organisationname.appendChild(doc.createTextNode(settings.MEDIA_ROOT+userExtension[0].defaultTemplateSet.organisationname))
    main.appendChild(organisationname)
    accountingPeriodTo = doc.createElement("accountingPeriodTo")
    accountingPeriodTo.appendChild(doc.createTextNode(self.end.year.__str__()))
    main.appendChild(accountingPeriodTo)
    accountingPeriodFrom = doc.createElement("accountingPeriodFrom")
    accountingPeriodFrom.appendChild(doc.createTextNode(self.begin.year.__str__()))
    main.appendChild(accountingPeriodFrom)
    accountingPeriodName = doc.createElement("headerpicture")
    accountingPeriodName.appendChild(doc.createTextNode(settings.MEDIA_ROOT+userExtension[0].defaultTemplateSet.logo.path))
    main.appendChild(accountingPeriodName)
    accountNumber = doc.createElement("AccountNumber")
    accounts = Account.objects.all()
    overallvalue = 0
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
          if account.accountType == "E":
            overallvalue = overallvalue + currentValue;
          if account.accountType == "S":
            overallvalue = overallvalue - currentValue;
    profitloss = doc.createElement("ProfitLoss")
    profitloss.appendChild(doc.createTextNode(overallvalue.__str__()))
    main.appendChild(profitloss)
    doc.appendChild(main)
    out.write(doc.toxml("utf-8"))
    out.close()
    check_output(['/usr/bin/fop', '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml', settings.PDF_OUTPUT_ROOT+'profitlossstatement_'+str(self.id)+'.xml', '-xsl', userExtension[0].defaultTemplateSet.profitLossStatementXSLFile.xslfile.path, '-pdf', settings.PDF_OUTPUT_ROOT+'profitlossstatement_'+str(self.id)+'.pdf'], stderr=STDOUT)
    return settings.PDF_OUTPUT_ROOT+"profitlossstatement_"+str(self.id)+".pdf"  
    
  def __unicode__(self):
      return  self.title

# TODO: def createNewAccountingPeriod() Neues Geschäftsjahr erstellen
   
  class Meta:
     app_label = "accounting"
     verbose_name = _('Accounting Period')
     verbose_name_plural = _('Accounting Periods')
            
class Account(models.Model):
   accountNumber = models.IntegerField(verbose_name=_("Account Number"))
   title = models.CharField(verbose_name=_("Account Title"), max_length=50)
   accountType = models.CharField(verbose_name=_("Account Type"), max_length=1, choices=ACCOUNTTYPECHOICES)
   description = models.TextField(verbose_name = _("Description"),null=True, blank=True) 
   originalAmount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Original Amount"), default=0.00) 
   isopenreliabilitiesaccount = models.BooleanField(verbose_name=_("Is The Open Liabilities Account"))
   isopeninterestaccount = models.BooleanField(verbose_name=_("Is The Open Interests Account"))
   isProductInventoryActiva = models.BooleanField(verbose_name=_("Is a Product Inventory Account"))
   isACustomerPaymentAccount = models.BooleanField(verbose_name=_("Is a Customer Payment Account"))
   
   def value(self):
      sum = self.allBookings(fromAccount = False) - self.allBookings(fromAccount = True)
      if (self.accountType == 'P' or self.accountType == 'E'):
        sum = 0 - sum
      return sum
      
   def valueNow(self, accountingPeriod):
      sum = self.allBookingsInAccountingPeriod(fromAccount = False, accountingPeriod = accountingPeriod) - self.allBookingsInAccountingPeriod(fromAccount = True, accountingPeriod = accountingPeriod)
      return sum
      
   def allBookings(self, fromAccount):
      sum = 0
      if (fromAccount == True):
         bookings = Booking.objects.filter(fromAccount=self.id)
      else:
         bookings = Booking.objects.filter(toAccount=self.id)
      
      for booking in list(bookings):
         sum = sum + booking.amount
         
      return sum

   def allBookingsInAccountingPeriod(self, fromAccount, accountingPeriod):
      sum = 0
      if (fromAccount == True):
         bookings = Booking.objects.filter(fromAccount=self.id, accountingPeriod=accountingPeriod.id)
      else:
         bookings = Booking.objects.filter(toAccount=self.id, accountingPeriod=accountingPeriod.id)
      
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
      
class ProductCategorie(models.Model):
   title = models.CharField(verbose_name=_("Product Categorie Title"), max_length=50)
   profitAccount = models.ForeignKey(Account, verbose_name=_("Profit Account"), limit_choices_to={"accountType" : "E"}, related_name="db_profit_account")
   lossAccount = models.ForeignKey(Account, verbose_name=_("Loss Account"),  limit_choices_to={"accountType" : "S"}, related_name="db_loss_account")
   
   class Meta:
      app_label = "accounting"
      verbose_name = _('Product Categorie')
      verbose_name_plural = _('Product Categories')
   def __unicode__(self):
      return  self.title

class Booking(models.Model):
   fromAccount = models.ForeignKey(Account, verbose_name=_("From Account"), related_name="db_booking_fromaccount")
   toAccount = models.ForeignKey(Account, verbose_name=_("To Account"), related_name="db_booking_toaccount")
   amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Amount"))
   description = models.CharField(verbose_name=_("Description"), max_length=120, null=True, blank=True)
   bookingReference = models.ForeignKey('crm.Invoice', verbose_name=_("Booking Reference"), null=True, blank=True)
   bookingDate = models.DateTimeField(verbose_name = _("Booking at"))
   accountingPeriod = models.ForeignKey(AccountingPeriod, verbose_name=_("AccountingPeriod"))
   staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Reference Staff"), related_name="db_booking_refstaff")
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"), auto_now=True)
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), auto_now_add=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Last modified by"), related_name="db_booking_lstmodified")
   
   def __unicode__(self):
      return  self.fromAccount.__str__()  + " " + self.toAccount.__str__()  + " " + self.amount.__str__() 
      
   class Meta:
      app_label = "accounting"
      verbose_name = _('Booking')
      verbose_name_plural = _('Bookings')
      
      
