# -*- coding: utf-8 -*-

from django.db import models
from const.accountTypeChoices import *
from crm.models import Contract
from django.utils.translation import ugettext as _
from os import system
from xml.dom.minidom import Document

   
class CRPCalculationUnit(models.Model):
   title =  models.CharField(max_length=200, verbose_name=_("Title")) # For example "Year 2009", "1st Quarter 2009"
   allEarnings = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name=_("All Earnings"))
   allSpendings = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name=_("All Spendings"))
   allActivas = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name=_("All Activas"))
   allPassivas = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name=_("All Passivas"))
   dateOfLastCalculation =  models.DateField(null=True, blank=True)
   begin = models.DateField()
   end = models.DateField()
              
   def calculateResults()
      earnings = 0;
      spendings = 0;
      passivas = 0;
      activas = 0;
      bookings = Bookings.objects.filter(crpCalculationUnit = self.id)
      for booking in list(bookings):
         if (booking.toAccount.accountType == 'E'):
            earnings += booking.amount
         elif (booking.toAccount.accountType == 'S'):
            spendings += booking.amount
         elif (booking.toAccount.accountType == 'P'):
            passivas += booking.amount
         elif (booking.toAccount.accountType == 'A'):
            activas += booking.amount
         if (booking.fromAccount.accountType == 'E'):
            earnings -= booking.amount
         elif (booking.fromAccount.accountType == 'S'):
            spendings -= booking.amount
         elif (booking.fromAccount.accountType == 'P'):
            passivas -= booking.amount
         elif (booking.fromAccount.accountType == 'A'):
            activas -= booking.amount
      self.allEarnings = earnings
      self.allSpendings = spendings
      self.allPassivas = passivas
      self.allActivas = activas
      self.save()
            
   def createBalanceSheetPDF(self)
      doc = Document()

      # Create the <wml> base element
      wml = doc.createElement("wml")
      doc.appendChild(wml)

      # Create the main <card> element
      maincard = doc.createElement("card")
      maincard.setAttribute("id", "main")
      wml.appendChild(maincard)

      # Create a <p> element
      paragraph1 = doc.createElement("p")
      maincard.appendChild(paragraph1)

      # Give the <p> elemenet some text
      ptext = doc.createTextNode("This is a test!")
      paragraph1.appendChild(ptext)

      # Print our newly created XML
      print doc.toprettyxml(indent="  ")


     system("fop -c /var/www/koalixcrm/verasans.xml -xml /tmp/balancesheet_"+str(self.id)+".xml -xsl /var/www/koalixcrm/balancesheet.xsl -pdf /tmp/balancesheet_"+str(self.id)+".pdf")
     
# TODO: def createProfitAndLossStatementPDF() Erfolgsrechnung

# TODO: def createNewCalculationUnit() Neues Geschäftsjahr erstellen
   
   class Meta:
      app_label = "crp"
      verbose_name = _('CRP Calculation Unit')
      verbose_name_plural = _('CRP Calculation Units')
           
class Account(models.Model):
   accountNumber = models.IntegerField(verbose_name=_("Account Number"))
   title = models.CharField(verbose_name=_("Account Title"), max_length=50)
   accountType = models.CharField(verbose_name=_("Account Type"), max_length=1, choices=ACCOUNTTYPECHOICES)
   
   
   def valueNow(self):
      sum = self.allBookings(fromAccount = False) - self.allBookings(fromAccount = True)
      return sum
   
   def allBookings(self, fromAccount, crpCalculationUnit):
      sum = 0
      if (fromAccount == True):
         bookings = Booking.objects.filter(fromAccount=self.id, crpCalculationUnit=crpCalculationUnit.id)
      else:
         bookings = Booking.objects.filter(toAccount=self.id, crpCalculationUnit=crpCalculationUnit.id)
      
      for booking in list(bookings):
         sum = sum + booking.amount
         
      return sum
      
   class Meta:
      app_label = "crp"
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
   crpCalculationUnit = models.ForeignKey(CRPCalculationUnit, verbose_name=_("CRPCalculationUnit"))
   staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Reference Staff"), related_name="db_booking_refstaff")
   dateofcreation = models.DateTimeField(auto_now_add=True, verbose_name = _("Created at"))
   lastmodification = models.DateTimeField(auto_now=True, verbose_name = _("Last modified"), null=True, blank=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Last modified by"), related_name="db_booking_lstmodified")
   
   class Meta:
      app_label = "crp"
      verbose_name = _('Booking')
      verbose_name_plural = _('Bookings')
