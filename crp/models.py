# -*- coding: utf-8 -*-

from django.db import models
from const.accountTypeChoices import *
from crm.models import Contract
from django.utils.translation import ugettext as _

   
class CRPCalculationUnit(models.Model):
   title =  models.CharField(max_length=200, verbose_name=_("Title")) # For example "Year 2009", "1st Quarter 2009"
   allEarnings = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name=_("All Earnings"))
   allSpendings = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name=_("All Spendings"))
   allActivas = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name=_("All Activas"))
   allPassivas = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name=_("All Passivas"))
   dateOfLastCalculation =  models.DateField(null=True, blank=True)
   begin = models.DateField()
   end = models.DateField()
# TODO:   isPartOf = models.ForeignKey(self, blank=True, null=True)
              
#   def calculateResults()
#      accounts = Account.objects.get(crpCalculationUnit = self.id)
#      if type(accounts) == Account:
#         accounts.accountType == 'E':
#            allEarings = 
#      else:
      
   
   class Meta:
      app_label = "crp"
      verbose_name = _('CRP Calculation Unit')
      verbose_name_plural = _('CRP Calculation Units')
           
class Account(models.Model):
   accountNumber = models.IntegerField(verbose_name=_("Account Number"))
   title = models.CharField(verbose_name=_("Account Title"), max_length=50)
   accountType = models.CharField(verbose_name=_("Account Type"), max_length=1, choices=ACCOUNTTYPECHOICES)
   
   class Meta:
      app_label = "crp"
      verbose_name = _('Account')
      verbose_name_plural = _('Account')
      ordering = ['accountNumber']
   

class AccountUsage(models.Model):
   account = models.ForeignKey(Account, verbose_name=_('Account Template'))
   crpCalculationUnit = models.ForeignKey(CRPCalculationUnit, verbose_name=_('CRP Calculation Unit'))
   valueAtStartOfBusinessYear = models.DecimalField(max_digits=20, decimal_places=2,verbose_name=_("Value at start of Business Year"))
   
   def valueNow(self):
      fromBookings = Booking.objects.filter(fromAccount=self.id)
      toBookings = Booking.objects.filter(toAccount=self.id)
      sum = 0
      if type(toBookings) == Booking:
         sum = sum + toBookings.amount
      else:
         for booking in toBookings:
            sum = sum + booking.amount
      if type(fromBookings) == Booking:
         sum = sum - fromBookings.amount
      else:
         for booking in fromBookings:
            sum = sum - booking.amount
      return sum
   
   class Meta:
      app_label = "crp"
      verbose_name = _('Account Relation to Calc. Unit')
      verbose_name_plural = _('Account Relations to Calc. Units')

class Booking(models.Model):
   fromAccount = models.ForeignKey(Account, verbose_name=_("From Account"), related_name="db_booking_fromaccount")
   toAccount = models.ForeignKey(Account, verbose_name=_("To Account"), related_name="db_booking_toaccount")
   amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Amount"))
   description = models.TextField(verbose_name=_("Description"), blank=True)
   bookingReference = models.ForeignKey(Contract, null=True, blank=True)
   bookingDate = models.DateTimeField(verbose_name = _("Booking at"))
   staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Reference Staff"), related_name="db_booking_refstaff")
   dateofcreation = models.DateTimeField(auto_now_add=True, verbose_name = _("Created at"))
   lastmodification = models.DateTimeField(auto_now=True, verbose_name = _("Last modified"), null=True, blank=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Last modified by"), related_name="db_booking_lstmodified")
   
   class Meta:
      app_label = "crp"
      verbose_name = _('Booking')
      verbose_name_plural = _('Bookings')
