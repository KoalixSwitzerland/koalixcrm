# -*- coding: utf-8 -*-

from django.db import models
from const.country import *
from const.postaladdressprefix import *
from const.purpose import *
from const.status import *
from django.db.models import signals
from middleware import threadlocals
from datetime import date
from datetime import timedelta
from django.utils.translation import ugettext as _
from decimal import Decimal
from os import system
from django.core import serializers
import copy
import settings
import djangoUserExtention
from django.contrib import auth

class Currency (models.Model):
   description = models.CharField(verbose_name = _("Description"), max_length=100)
   shortName = models.CharField(verbose_name = _("Displayed Name After Price In The Position"), max_length=3)
   rounding = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = _("Rounding"), blank=True, null=True)

   def __unicode__(self):
      return  self.shortName
   
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Currency')
      verbose_name_plural = _('Currency') 
   
class PostalAddress(models.Model):
   prefix = models.CharField(max_length=1, choices=POSTALADDRESSPREFIX, verbose_name = _("Prefix"), blank=True, null=True)
   name = models.CharField(max_length=100, verbose_name = _("Name"), blank=True, null=True)
   prename = models.CharField(max_length=100, verbose_name = _("Prename"), blank=True, null=True)
   addressline1 = models.CharField(max_length=200, verbose_name = _("Addressline 1"), blank=True, null=True)
   addressline2 = models.CharField(max_length=200, verbose_name = _("Addressline 2"), blank=True, null=True)
   addressline3 = models.CharField(max_length=200, verbose_name = _("Addressline 3"), blank=True, null=True)
   addressline4 = models.CharField(max_length=200, verbose_name = _("Addressline 4"), blank=True, null=True)
   zipcode = models.IntegerField(verbose_name = _("Zipcode"), blank=True, null=True)
   town = models.CharField(max_length=100, verbose_name = _("City"), blank=True, null=True)
   state = models.CharField(max_length=100, verbose_name = _("State"), blank=True, null=True)
   country = models.CharField(max_length=2, choices=[(x[0], x[3]) for x in COUNTRIES], verbose_name = _("Country"), blank=True, null=True)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Postal Address')
      verbose_name_plural = _('Postal Address')

class PhoneAddress(models.Model):
   phone = models.CharField(max_length=20, verbose_name = _("Phone Number"))

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Phone Address')
      verbose_name_plural = _('Phone Address')

class EmailAddress(models.Model):
   email = models.EmailField(max_length=200, verbose_name = _("Email Address"))

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Email Address')
      verbose_name_plural = _('Email Address')

class Contact(models.Model):
   name = models.CharField(max_length=300, verbose_name = _("Name"))
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"))
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Last modified by"), editable=True)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Contact')
      verbose_name_plural = _('Contact')

class ModeOfPayment(models.Model):
   name = models.CharField(max_length=300, verbose_name = _("Name"))
   timeToPaymentDate = models.IntegerField(verbose_name = _("Days To Payment Date"))
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Mode of Payment')
      verbose_name_plural = _('Modes of Payment')

   def __unicode__(self):
      return str(self.id) + ' ' + self.name

class CustomerGroup(models.Model):
   name = models.CharField(max_length=300)
      
   def __unicode__(self):
      return str(self.id) + ' ' + self.name
      
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Customer Group')
      verbose_name_plural = _('Customer Groups')

class Customer(Contact):
   defaultModeOfPayment = models.ForeignKey('ModeOfPayment', verbose_name= _('Default Mode of Payment'))
   ismemberof = models.ManyToManyField(CustomerGroup, verbose_name = _('Is member of'), blank=True, null=True)
   
   def createContract(self):
      contract = Contract()
      contract.defaultcustomer = self
      contract.save()
      return contract
   
   def createInvoice(self):
      contract = self.createContract()
      invoice = contract.createInvoice()
      return invoice
      
   def createQuote(self):
      contract = self.createContract()
      quote = contract.createQuote()
      return quote

   def isInGroup(self, customerGroup):
      for customerGroupMembership in self.ismemberof.all():
         if (customerGroupMembership.id == customerGroup.id):
            return 1
      return 0
   
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Customer')
      verbose_name_plural = _('Customers')

   def __unicode__(self):
      return str(self.id) + ' ' + self.name

class Distributor(Contact):
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Distributor')
      verbose_name_plural = _('Distributors')

   def __unicode__(self):
      return str(self.id) + ' ' + self.name

class ShipmentPartner(Contact):
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Shipment Partner')
      verbose_name_plural = _('Shipment Partner')

   def __unicode__(self):
      return str(self.id) + ' ' + self.name

class Contract(models.Model):
   staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Staff"), related_name="db_relcontractstaff")
   description = models.TextField(verbose_name = _("Description"))
   defaultcustomer = models.ForeignKey(Customer, verbose_name = _("Default Customer"), null=True, blank=True)
   defaultdistributor = models.ForeignKey(Distributor, verbose_name = _("Default Distributor"), null=True, blank=True)
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"))
   defaultcurrency = models.ForeignKey(Currency, verbose_name=_("Default Currency"), blank=False, null=False)
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name = _("Last modified by"), related_name="db_contractlstmodified")

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Contract')
      verbose_name_plural = _('Contracts')
      
   def createInvoice(self):
      invoice = Invoice()
      invoice.contract = self
      invoice.discount = 0
      invoice.customer = self.defaultcustomer
      invoice.status = 'C'
      invoice.currency = self.defaultcurrency
      invoice.payableuntil = date.today()+timedelta(days=self.defaultcustomer.defaultModeOfPayment.timeToPaymentDate)
      invoice.dateofcreation = date.today().__str__()
      invoice.save()
      return invoice
      
   def createQuote(self):
      quote = Quote()
      quote.contract = self
      quote.discount = 0
      quote.customer = self.defaultcustomer
      quote.status = 'C'
      quote.currency = self.defaultcurrency
      quote.validuntil = date.today().__str__()
      quote.dateofcreation = date.today().__str__()
      quote.save()
      return quote
      
   def createPurchaseOrder(self):
      purchaseorder = PurchaseOrder()
      purchaseorder.contract = self
      purchaseorder.description = self.description
      purchaseorder.discount = 0
      purchaseorder.currency = self.defaultcurrency
      purchaseorder.distributor = self.defaultdistributor
      purchaseorder.status = 'C'
      purchaseorder.dateofcreation = date.today().__str__()
# TODO: today is not correct it has to be replaced
      purchaseorder.save()
      return purchaseorder

   def __unicode__(self):
      return _("Contract") + " " + str(self.id)

class PurchaseOrder(models.Model):
   contract = models.ForeignKey(Contract, verbose_name = _("Contract"))
   externalReference = models.CharField(verbose_name = _("External Reference"), max_length=100, blank=True, null=True)
   distributor = models.ForeignKey(Distributor, verbose_name = _("Distributor"))
   description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True)
   lastPricingDate = models.DateField(verbose_name = _("Last Pricing Date"), blank=True, null=True)
   lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Price With Tax"), blank=True, null=True)
   lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"), blank=True, null=True)
   status = models.CharField(max_length=1, choices=PURCHASEORDERSTATUS)
   staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Staff"), related_name="db_relpostaff")
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"))
   currency = models.ForeignKey(Currency, verbose_name=_("Currency"), blank=False, null=False)
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name = _("Last modified by"), related_name="db_polstmodified")
   
   def recalculatePrices(self, pricingDate):
      price = 0
      tax = 0
      try:
         positions = PurchaseOrderPosition.objects.filter(contract=self.id)
         if type(positions) == PurchaseOrderPosition:
            if type(self.discount) == Decimal:
               price = int(positions.recalculatePrices(pricingDate, self.customer, self.currency)*(1-self.discount/100)/self.currency.rounding)*self.currency.rounding
               tax = int(positions.recalculateTax(self.currency)*(1-self.discount/100)/self.currency.rounding)*self.currency.rounding
            else:
               price = positions.recalculatePrices(pricingDate, self.customer, self.currency)
               tax = positions.recalculateTax(self.currency)
         else:
            for position in positions:
               if type(self.discount) == Decimal:
                  price += int(position.recalculatePrices(pricingDate, self.customer, self.currency)*(1-self.discount/100)/self.currency.rounding)*self.currency.rounding
                  tax += int(position.recalculateTax(self.currency)*(1-self.discount/100)/self.currency.rounding)*self.currency.rounding
               else:
                  price += position.recalculatePrices(pricingDate, self.customer, self.currency)
                  tax += position.recalculateTax(self.currency)
         self.lastCalculatedPrice = price
         self.lastCalculatedTax = tax
         self.lastPricingDate = pricingDate
         self.save()
         return 1
      except Quote.DoesNotExist:  
         return 0
         
   def createPDF(self, purchaseconfirmation):
     XMLSerializer = serializers.get_serializer("xml")
     xml_serializer = XMLSerializer()
     out = open("/tmp/purchaseorder_"+str(self.id)+".xml", "w")
     objectsToSerialize = list(PurchaseOrder.objects.filter(id=self.id)) 
     objectsToSerialize += list(Contact.objects.filter(id=self.distributor.id))
     objectsToSerialize += list(Currency.objects.filter(id=self.currency.id))
     objectsToSerialize += list(PurchaseOrderPosition.objects.filter(contract=self.id))
     for position in list(PurchaseOrderPosition.objects.filter(contract=self.id)):
         objectsToSerialize += list(Position.objects.filter(id=position.id))
         objectsToSerialize += list(Product.objects.filter(id=position.product.id))
         objectsToSerialize += list(Unit.objects.filter(id=position.unit.id))
     objectsToSerialize += list(auth.models.User.objects.filter(id=self.staff.id))
     userExtention = djangoUserExtention.models.UserExtention.objects.filter(user=self.staff.id)
     objectsToSerialize += list(userExtention)
     templateset = djangoUserExtention.models.TemplateSet.objects.filter(id=userExtention[0].defaultTemplateSet.id)
     objectsToSerialize += list(templateset)
     objectsToSerialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
     objectsToSerialize += list(PostalAddressForContact.objects.filter(person=self.distributor.id))
     for address in list(PostalAddressForContact.objects.filter(person=self.distributor.id)):
         objectsToSerialize += list(PostalAddress.objects.filter(id=address.id))
     xml_serializer.serialize(objectsToSerialize, stream=out, indent=3)
     out.close()
     system('bash -c "fop -c /var/www/koalixcrm/verasans.xml -xml /tmp/purchaseorder_'+str(self.id)+'.xml -xsl ' + settings.MEDIA_ROOT+userExtention[0].defaultTemplateSet.purchaseorderXSLFile.xslfile.name+' -pdf /tmp/purchaseorder_'+str(self.id)+'.pdf"')
     return "/tmp/purchaseorder_"+str(self.id)+".pdf"    

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Purchase Order')
      verbose_name_plural = _('Purchase Order')

   def __unicode__(self):
      return _("Purchase Order")+ ": " + str(self.id) + " "+ _("from Contract") + ": " + str(self.contract.id) 

class SalesContract(models.Model):
   contract = models.ForeignKey(Contract, verbose_name=_('Contract'))
   externalReference = models.CharField(verbose_name = _("External Reference"), max_length=100, blank=True)
   discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = _("Discount"), blank=True, null=True)
   description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True)
   lastPricingDate = models.DateField(verbose_name = _("Last Pricing Date"), blank=True, null=True)
   lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Price With Tax"), blank=True, null=True)
   lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"), blank=True, null=True)
   customer = models.ForeignKey(Customer, verbose_name = _("Customer"))
   staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Staff"), related_name="db_relscstaff")
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"))
   currency = models.ForeignKey(Currency, verbose_name=_("Currency"), blank=False, null=False)
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name = _("Last modified by"), related_name="db_lstscmodified")
      
   def recalculatePrices(self, pricingDate):
      price = 0
      tax = 0
      try:
         positions = SalesContractPosition.objects.filter(contract=self.id)
         if type(positions) == SalesContractPosition:
            if type(self.discount) == Decimal:
               price = int(positions.recalculatePrices(pricingDate, self.customer, selof.currency)*(1-self.discount/100)/self.currency.rounding)*self.currency.rounding
               tax = int(positions.recalculateTax(self.currency)*(1-self.discount/100)/self.currency.rounding)*self.currency.rounding
            else:
               price = positions.recalculatePrices(pricingDate, self.customer, self.currency)
               tax = positions.recalculateTax(self.currency)
         else:
            for position in positions:
               price += position.recalculatePrices(pricingDate, self.customer, self.currency)
               tax += position.recalculateTax(self.currency)
            if type(self.discount) == Decimal:
               price = int(price*(1-self.discount/100)/self.currency.rounding)*self.currency.rounding
               tax = int(tax*(1-self.discount/100)/self.currency.rounding)*self.currency.rounding

         self.lastCalculatedPrice = price
         self.lastCalculatedTax = tax
         self.lastPricingDate = pricingDate
         self.save()
         return 1
      except Quote.DoesNotExist:  
         return 0

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Sales Contract')
      verbose_name_plural = _('Sales Contracts')

   def __unicode__(self):
      return _("Sales Contract")+ ": " + str(self.id) + " "+_("from Contract")+": " + str(self.contract.id) 
      
class Quote(SalesContract):
   validuntil = models.DateField(verbose_name = _("Valid until"))
   status = models.CharField(max_length=1, choices=QUOTESTATUS, verbose_name=_('Status'))

   def createInvoice(self):
      invoice = Invoice()
      invoice.contract = self.contract
      invoice.description = self.description
      invoice.discount = self.discount
      invoice.customer = self.customer
      invoice.status = 'C'
      invoice.derivatedFromQuote = self
      invoice.currency = self.currency
      invoice.payableuntil = date.today()+timedelta(days=self.customer.defaultModeOfPayment.timeToPaymentDate)
      invoice.dateofcreation = date.today().__str__()
      invoice.modeOfPayment = self.customer.defaultModeOfPayment
# TODO: today is not correct it has to be replaced
      invoice.save()
      try:
         quotePositions = SalesContractPosition.objects.filter(contract=self.id)
         for quotePosition in list(quotePositions):
            invoicePosition = SalesContractPosition()
            invoicePosition.product = quotePosition.product 
            invoicePosition.positionNumber = quotePosition.positionNumber 
            invoicePosition.quantity = quotePosition.quantity 
            invoicePosition.description = quotePosition.description 
            invoicePosition.discount = quotePosition.discount 
            invoicePosition.product = quotePosition.product 
            invoicePosition.unit = quotePosition.unit 
            invoicePosition.sentOn = quotePosition.sentOn 
            invoicePosition.shipmentPartner = quotePosition.shipmentPartner 
            invoicePosition.shipmentID = quotePosition.shipmentID 
            invoicePosition.overwriteProductPrice = quotePosition.overwriteProductPrice 
            invoicePosition.positionPricePerUnit = quotePosition.positionPricePerUnit 
            invoicePosition.lastPricingDate = quotePosition.lastPricingDate 
            invoicePosition.lastCalculatedPrice = quotePosition.lastCalculatedPrice 
            invoicePosition.lastCalculatedTax = quotePosition.lastCalculatedTax 
            invoicePosition.contract = invoice 
            invoicePosition.save()
         return invoice
      except Quote.DoesNotExist:  
         return

   def createPDF(self, purchaseconfirmation):
     XMLSerializer = serializers.get_serializer("xml")
     xml_serializer = XMLSerializer()
     out = open("/tmp/quote_"+str(self.id)+".xml", "w")
     objectsToSerialize = list(Quote.objects.filter(id=self.id)) 
     objectsToSerialize += list(SalesContract.objects.filter(id=self.id)) 
     objectsToSerialize += list(Contact.objects.filter(id=self.customer.id))
     objectsToSerialize += list(Currency.objects.filter(id=self.currency.id))
     objectsToSerialize += list(SalesContractPosition.objects.filter(contract=self.id))
     for position in list(SalesContractPosition.objects.filter(contract=self.id)):
         objectsToSerialize += list(Position.objects.filter(id=position.id))
         objectsToSerialize += list(Product.objects.filter(id=position.product.id))
         objectsToSerialize += list(Unit.objects.filter(id=position.unit.id))
     objectsToSerialize += list(auth.models.User.objects.filter(id=self.staff.id))
     userExtention = djangoUserExtention.models.UserExtention.objects.filter(user=self.staff.id)
     objectsToSerialize += list(userExtention)
     templateset = djangoUserExtention.models.TemplateSet.objects.filter(id=userExtention[0].defaultTemplateSet.id)
     objectsToSerialize += list(templateset)
     objectsToSerialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
     objectsToSerialize += list(PostalAddressForContact.objects.filter(person=self.customer.id))
     for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
         objectsToSerialize += list(PostalAddress.objects.filter(id=address.id))
     xml_serializer.serialize(objectsToSerialize, stream=out, indent=3)
     out.close()
     if (purchaseconfirmation == False) :
         system('bash -c "fop -c /var/www/koalixcrm/verasans.xml -xml /tmp/quote_'+str(self.id)+'.xml -xsl ' + settings.MEDIA_ROOT+userExtention[0].defaultTemplateSet.quoteXSLFile.xslfile.name+' -pdf /tmp/quote_'+str(self.id)+'.pdf"')
     else:
         system('bash -c "fop -c /var/www/koalixcrm/verasans.xml -xml /tmp/quote_'+str(self.id)+'.xml -xsl ' + settings.MEDIA_ROOT+userExtention[0].defaultTemplateSet.purchaseconfirmationXSLFile.xslfile.name+' -pdf /tmp/purchaseconfirmation_'+str(self.id)+'.pdf"')
     return "/tmp/quote_"+str(self.id)+".pdf"
     
   def __unicode__(self):
      return _("Quote")+ ": " + str(self.id) + " "+_("from Contract")+": " + str(self.contract.id) 
      
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Quote')
      verbose_name_plural = _('Quotes')

class Invoice(SalesContract):
   payableuntil = models.DateField(verbose_name = _("To pay until"))
   derivatedFromQuote = models.ForeignKey(Quote, blank=True, null=True)
   paymentBankReference = models.CharField(verbose_name = _("Payment Bank Reference"), max_length=100, blank=True)
   status = models.CharField(max_length=1, choices=INVOICESTATUS)      
   
   def createFromContract(contract):
      invoice.contract = contract
      invoice.discount = 0
      invoice.customer = contract.defaultcustomer
      invoice.status = 'C'
      invoice.payableuntil = date.today().__str__()
      invoice.dateofcreation = date.today().__str__()
      invoice.modeOfPayment = contract.defaultcustomer.defaultModeOfPayment
# TODO: today is not correct it has to be replaced

   def createPDF(self, deliveryorder):
     XMLSerializer = serializers.get_serializer("xml")
     xml_serializer = XMLSerializer()
     out = open("/tmp/invoice_"+str(self.id)+".xml", "w")
     objectsToSerialize = list(Invoice.objects.filter(id=self.id)) 
     objectsToSerialize += list(SalesContract.objects.filter(id=self.id)) 
     objectsToSerialize += list(Contact.objects.filter(id=self.customer.id))
     objectsToSerialize += list(Currency.objects.filter(id=self.currency.id))
     objectsToSerialize += list(SalesContractPosition.objects.filter(contract=self.id))
     for position in list(SalesContractPosition.objects.filter(contract=self.id)):
         objectsToSerialize += list(Position.objects.filter(id=position.id))
         objectsToSerialize += list(Product.objects.filter(id=position.product.id))
         objectsToSerialize += list(Unit.objects.filter(id=position.unit.id))
     objectsToSerialize += list(auth.models.User.objects.filter(id=self.staff.id))
     userExtention = djangoUserExtention.models.UserExtention.objects.filter(user=self.staff.id)
     objectsToSerialize += list(userExtention)
     templateset = djangoUserExtention.models.TemplateSet.objects.filter(id=userExtention[0].defaultTemplateSet.id)
     objectsToSerialize += list(templateset)
     objectsToSerialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
     objectsToSerialize += list(PostalAddressForContact.objects.filter(person=self.customer.id))
     for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
         objectsToSerialize += list(PostalAddress.objects.filter(id=address.id))
     xml_serializer.serialize(objectsToSerialize, stream=out, indent=3)
     out.close()
     if (deliveryorder == False):
        system('bash -c "fop -c /var/www/koalixcrm/verasans.xml -xml /tmp/invoice_'+str(self.id)+'.xml -xsl ' + settings.MEDIA_ROOT+userExtention[0].defaultTemplateSet.invoiceXSLFile.xslfile.name+' -pdf /tmp/invoice_'+str(self.id)+'.pdf"')
     else:
        system('bash -c "fop -c /var/www/koalixcrm/verasans.xml -xml /tmp/invoice_'+str(self.id)+'.xml -xsl ' + settings.MEDIA_ROOT+userExtention[0].defaultTemplateSet.deilveryorderXSLFile.xslfile.name+' -pdf /tmp/deliveryorder_'+str(self.id)+'.pdf"')
     return "/tmp/invoice_"+str(self.id)+".pdf"

#  TODO: def registerPayment(self, amount, registerpaymentinaccounting):
   def __unicode__(self):
      return _("Invoice")+ ": " + str(self.id) + " "+_("from Contract")+": " + str(self.contract.id) 
      
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Invoice')
      verbose_name_plural = _('Invoices') 
   
class Unit(models.Model):
   description = models.CharField(verbose_name = _("Description"), max_length=100)
   shortName = models.CharField(verbose_name = _("Displayed Name After Quantity In The Position"), max_length=3)
   isAFractionOf = models.ForeignKey('self', blank=True, null=True, verbose_name = _("Is A Fraction Of"))
   fractionFactorToNextHigherUnit = models.IntegerField(verbose_name = _("Factor Between This And Next Higher Unit"), blank=True, null=True)

   def __unicode__(self):
      return  self.shortName

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Unit')
      verbose_name_plural = _('Units') 

class Tax(models.Model):
   taxrate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = _("Taxrate in Percentage"))
   name = models.CharField(verbose_name = _("Taxname"), max_length=100)

   def getTaxRate(self):
      return self.taxrate;

   def __unicode__(self):
      return  self.name

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Tax')
      verbose_name_plural = _('Taxes') 
      
	
class Product(models.Model):
   description = models.TextField(verbose_name = _("Description"), blank=True) 
   title = models.CharField(verbose_name = _("Title"), max_length=200)
   productNumber = models.IntegerField(verbose_name = _("Product Number"))
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"))
   defaultunit = models.ForeignKey(Unit, verbose_name = _("Unit"))
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name = _("Last modified by"))
   tax = models.ForeignKey(Tax, blank=False)

   def getPrice(self, date, unit, customer, currency):
      prices = Price.objects.filter(product=self.id)
      unitTransforms = UnitTransform.objects.filter(product=self.id)
      customerGroupTransforms = CustomerGroupTransform.objects.filter(product=self.id)
      validpriceslist = list()
      for price in list(prices):
         for customerGroup in CustomerGroup.objects.filter(customer=customer):
            if price.matchesDateUnitCustomerGroupCurrency(date, unit, customerGroup, currency):
               validpriceslist.append(price.price);
            else:
               for customerGroupTransform in customerGroupTransforms:
                  if price.matchesDateUnitCustomerGroupCurrency(date, unit, customerGroupTransfrom.transform(customerGroup), currency):
                     validpriceslist.append(price.price*customerGroup.factor);
                  else:
                     for unitTransfrom in list(unitTransforms):
                        if price.matchesDateUnitCustomerGroupCurrency(date, unitTransfrom.transfrom(unit).transform(unitTransfrom), customerGroupTransfrom.transform(customerGroup), currency):
                           validpriceslist.append(price.price*customerGroupTransform.factor*unitTransform.factor);
      if (len(validpriceslist) >0):
         lowestprice = validpriceslist[0]
         for price in validpriceslist:
            if (price < lowestprice):
               lowestprice = price
         return lowestprice
      else:           
         raise Product.NoPriceFound(customer, unit, date, self)

   def getTaxRate(self):
      return self.tax.getTaxRate();

   def __unicode__(self):
      return str(self.productNumber) + ' ' + self.title

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Product')
      verbose_name_plural = _('Products')
      
   class NoPriceFound(Exception):
     def __init__(self, customer, unit, date, product):
       self.customer = customer
       self.unit = unit
       self.date = date
       self.product = product
       return 
     def __str__ (self):
       return _("There is no Price for this product")+": "+ self.product.__unicode__() + _("that matches the date")+": "+self.date.__str__() +" ,"+ _("customer")+ ": " +self.customer.__unicode__()+_(" and unit")+":"+ self.unit.__unicode__()

      
class UnitTransform(models.Model):
   fromUnit = models.ForeignKey('Unit', verbose_name = _("From Unit"), related_name="db_reltransfromfromunit")
   toUnit = models.ForeignKey('Unit', verbose_name = _("To Unit"), related_name="db_reltransfromtounit")
   product = models.ForeignKey('Product', verbose_name = _("Product"))
   factor = models.IntegerField(verbose_name = _("Factor between From and To Unit"), blank=True, null=True)

   def transform(self, unit):
      if (self.fromUnit == unit):
         return self.toUnit
      else:
         return unit
         
   def __unicode__(self):
      return  "From " + self.fromUnit.shortName + " to " + self.toUnit.shortName

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Unit Transfrom')
      verbose_name_plural = _('Unit Transfroms') 
           
class CustomerGroupTransform(models.Model):
   fromCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name = _("From Unit"), related_name="db_reltransfromfromcustomergroup")
   toCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name = _("To Unit"), related_name="db_reltransfromtocustomergroup")
   product = models.ForeignKey('Product', verbose_name = _("Product"))
   factor = models.IntegerField(verbose_name = _("Factor between From and To Customer Group"), blank=True, null=True)

   def transform(self, customerGroup):
      if (self.fromCustomerGroup == customerGroup):
         return self.toCustomerGroup
      else:
         return unit
         
   def __unicode__(self):
      return  "From " + self.fromCustomerGroup.name + " to " + self.toCustomerGroup.name

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Customer Group Price Transfrom')
      verbose_name_plural = _('Customer Group Price Transfroms') 
           
class Price(models.Model):
   product = models.ForeignKey(Product, verbose_name = _("Product"))
   unit = models.ForeignKey(Unit, blank=False, verbose_name= _("Unit"))
   currency = models.ForeignKey(Currency, blank=False, null=False, verbose_name=('Currency'))
   customerGroup = models.ForeignKey(CustomerGroup, blank=True, null=True, verbose_name = _("Customer Group"))
   price = models.DecimalField(max_digits=17, decimal_places=2, verbose_name = _("Price Per Unit"))
   validfrom = models.DateField(verbose_name = _("Valid from"), blank=True, null=True)
   validuntil = models.DateField(verbose_name = _("Valid until"), blank=True, null=True)

   def matchesDateUnitCustomerGroupCurrency(self, date, unit, customerGroup, currency):
      if self.validfrom == None:
        if self.validuntil == None:
          if self.customerGroup == None:
            if (unit == self.unit) & (self.currency == currency):
              return 1
          else:
            if (unit == self.unit) & (self.customerGroup == customerGroup) & (self.currency == currency): 
              return 1
        elif self.customerGroup == None:
          if ((date - self.validuntil).days < 0) & (unit == self.unit) & (self.currency == currency):
            return 1
        else:
          if ((date - self.validuntil).days < 0) & (unit == self.unit) & (self.customerGroup == customerGroup) & (self.currency == currency):
            return 1
      elif self.validuntil == None:
        if self.customerGroup == None:
          if ((self.validfrom - date).days < 0) & (unit == self.unit) & (self.currency == currency):
            return 1
        else:
          if ((self.validfrom - date).days < 0) & (unit == self.unit) & (self.customerGroup == customerGroup) & (self.currency == currency):
            return 1
      elif self.customerGroup == None:
        if ((self.validfrom - date).days < 0) & (self.validuntil== None) & (unit == self.unit) & (self.customerGroup == None) & (self.currency == currency):
          return 1
      else:
        if ((self.validfrom - date).days < 0) & ((date - self.validuntil).days < 0) & (unit == self.unit) & (self.customerGroup == customerGroup) & (self.currency == currency):
          return 1

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Price')
      verbose_name_plural = _('Prices')

class Position(models.Model):
   positionNumber = models.IntegerField(verbose_name = _("Position Number"))
   quantity = models.IntegerField(verbose_name = _("Quantity"))
   description = models.TextField(verbose_name = _("Description"), blank=True, null=True)
   discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = _("Discount"), blank=True, null=True)
   product = models.ForeignKey(Product, verbose_name = _("Product"), blank=True, null=True)
   unit = models.ForeignKey(Unit, verbose_name = _("Unit"), blank=True, null=True)
   sentOn = models.DateField(verbose_name = _("Shipment on"), blank=True, null=True)
   shipmentPartner = models.ForeignKey(ShipmentPartner, verbose_name = _("Shipment Partner"), blank=True, null=True)
   shipmentID = models.CharField(max_length=100, verbose_name = _("Shipment ID"), blank=True, null=True)
   overwriteProductPrice = models.BooleanField(verbose_name=_('Overwrite Product Price'))
   positionPricePerUnit = models.DecimalField(verbose_name=_("Price Per Unit"), max_digits=17, decimal_places=2, blank=True, null=True)
   lastPricingDate = models.DateField(verbose_name = _("Last Pricing Date"), blank=True, null=True)
   lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Price"), blank=True, null=True)
   lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"), blank=True, null=True)

   def recalculatePrices(self, pricingDate, customer, currency):
     if self.overwriteProductPrice == False:
       self.positionPricePerUnit = self.product.getPrice(pricingDate, self.unit, customer, currency)
     if type(self.discount) == Decimal:
       self.lastCalculatedPrice = int(self.positionPricePerUnit*self.quantity*(1-self.discount/100)/currency.rounding)*currency.rounding
     else:
       self.lastCalculatedPrice = self.positionPricePerUnit*self.quantity
     self.lastPricingDate = pricingDate
     self.save()
     return self.lastCalculatedPrice
     
   def recalculateTax(self, currency):
     if type(self.discount) == Decimal:
       self.lastCalculatedTax = int(self.product.getTaxRate()/100*self.positionPricePerUnit*self.quantity*(1-self.discount/100)/currency.rounding)*currency.rounding
     else:
       self.lastCalculatedTax = self.product.getTaxRate()/100*self.positionPricePerUnit*self.quantity
     self.save()
     return self.lastCalculatedTax
     
   def __unicode__(self):
      return _("Position")+ ": " + str(self.id)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Position')
      verbose_name_plural = _('Positions')

class SalesContractPosition(Position):
   contract = models.ForeignKey(SalesContract, verbose_name = _("Contract"))
   
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Salescontract Position')
      verbose_name_plural = _('Salescontract Positions')
      
   def __unicode__(self):
      return _("Salescontract Position")+ ": " + str(self.id)


class PurchaseOrderPosition(Position):
   contract = models.ForeignKey(PurchaseOrder, verbose_name = _("Contract"))
   
   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Purchaseorder Position')
      verbose_name_plural = _('Purchaseorder Positions')
      
   def __unicode__(self):
      return _("Purchaseorder Position")+ ": " + str(self.id)

class PhoneAddressForContact(PhoneAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
   person = models.ForeignKey(Contact)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Phone Address For Contact')
      verbose_name_plural = _('Phone Address For Contact')

   def __unicode__(self):
      return str(self.phone)

class EmailAddressForContact(EmailAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
   person = models.ForeignKey(Contact)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Email Address For Contact')
      verbose_name_plural = _('Email Address For Contact')

   def __unicode__(self):
      return str(self.email)

class PostalAddressForContact(PostalAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
   person = models.ForeignKey(Contact)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Postal Address For Contact')
      verbose_name_plural = _('Postal Address For Contact')

   def __unicode__(self):
      return self.prename + ' ' + self.name + ' ' + self.addressline1
   
class PostalAddressForContract(PostalAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(Contract)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Postal Address For Contracts')
      verbose_name_plural = _('Postal Address For Contracts')

   def __unicode__(self):
      return self.prename + ' ' + self.name + ' ' + self.addressline1
   
class PostalAddressForPurchaseOrder(PostalAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(PurchaseOrder)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Postal Address For Contracts')
      verbose_name_plural = _('Postal Address For Contracts')

   def __unicode__(self):
      return self.prename + ' ' + self.name + ' ' + self.addressline1
   
class PostalAddressForSalesContract(PostalAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(SalesContract)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Postal Address For Contracts')
      verbose_name_plural = _('Postal Address For Contracts')

   def __unicode__(self):
      return self.prename + ' ' + self.name + ' ' + self.addressline1

class PhoneAddressForContract(PhoneAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(Contract)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Phone Address For Contracts')
      verbose_name_plural = _('Phone Address For Contracts')

   def __unicode__(self):
      return str(self.phone)

class PhoneAddressForSalesContract(PhoneAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(SalesContract)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Phone Address For Contracts')
      verbose_name_plural = _('Phone Address For Contracts')

   def __unicode__(self):
      return str(self.phone)

class PhoneAddressForPurchaseOrder(PhoneAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(PurchaseOrder)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Phone Address For Contracts')
      verbose_name_plural = _('Phone Address For Contracts')

   def __unicode__(self):
      return str(self.phone)

class EmailAddressForContract(EmailAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT) 
   contract = models.ForeignKey(Contract)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Email Address For Contracts')
      verbose_name_plural = _('Email Address For Contracts')

   def __unicode__(self):
      return str(self.email)

class EmailAddressForSalesContract(EmailAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT) 
   contract = models.ForeignKey(SalesContract)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Email Address For Contracts')
      verbose_name_plural = _('Email Address For Contracts')

   def __unicode__(self):
      return str(self.email)

class EmailAddressForPurchaseOrder(EmailAddress):
   purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT) 
   contract = models.ForeignKey(PurchaseOrder)

   class Meta:
      app_label = "crm"
      app_label_koalix = _('Customer Relationship Management (CRM)')
      verbose_name = _('Email Address For Contracts')
      verbose_name_plural = _('Email Address For Contracts')

   def __unicode__(self):
      return str(self.email)

def postInitAutoUserHandler(sender, instance, **kwarg):
   instance.staff = threadlocals.get_current_user()
   instance.dateofcreation = date.today().__str__()

def preSaveAutoNowUserHandler(sender, instance, **kwarg):
   instance.lastmodifiedby = threadlocals.get_current_user()
   instance.lastmodification = date.today().__str__()
   if instance is PurchaseOrder:
      instance.overwriteProductPrice = True;

signals.post_init.connect(postInitAutoUserHandler, Invoice)
signals.post_init.connect(postInitAutoUserHandler, Quote)
signals.post_init.connect(postInitAutoUserHandler, Contract)
signals.post_init.connect(postInitAutoUserHandler, PurchaseOrder)
signals.post_init.connect(postInitAutoUserHandler, Customer)
signals.post_init.connect(postInitAutoUserHandler, Distributor)
signals.post_init.connect(postInitAutoUserHandler, ShipmentPartner)
signals.post_init.connect(postInitAutoUserHandler, Product)
signals.pre_save.connect(preSaveAutoNowUserHandler, Invoice)
signals.pre_save.connect(preSaveAutoNowUserHandler, Quote)
signals.pre_save.connect(preSaveAutoNowUserHandler, Contract)
signals.pre_save.connect(preSaveAutoNowUserHandler, PurchaseOrder)
signals.pre_save.connect(preSaveAutoNowUserHandler, Customer)
signals.pre_save.connect(preSaveAutoNowUserHandler, Distributor)
signals.pre_save.connect(preSaveAutoNowUserHandler, ShipmentPartner)
signals.pre_save.connect(preSaveAutoNowUserHandler, Product)