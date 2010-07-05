# -*- coding: utf-8 -*-

from django.db import models
from const.country import *
from const.postaladdressprefix import *
from const.purpose import *
from const.status import *
from django.db.models import signals
from middleware import threadlocals
from datetime import date
from django.utils.translation import ugettext as _
from decimal import Decimal
import libxslt
import libxml2
from django.core import serializers
import copy
from django.contrib import auth

class PostalAddress(models.Model):
   prefix = models.CharField(max_length=1, choices=POSTALADDRESSPREFIX, verbose_name = _("Prefix"), blank=True)
   name = models.CharField(max_length=100, verbose_name = _("Name"), blank=True)
   prename = models.CharField(max_length=100, verbose_name = _("Prename"), blank=True)
   addressline1 = models.CharField(max_length=200, verbose_name = _("Addressline 1"), blank=True)
   addressline2 = models.CharField(max_length=200, verbose_name = _("Addressline 2"), blank=True)
   addressline3 = models.CharField(max_length=200, verbose_name = _("Addressline 3"), blank=True)
   addressline4 = models.CharField(max_length=200, verbose_name = _("Addressline 4"), blank=True)
   zipcode = models.IntegerField(verbose_name = _("Zipcode"), blank=True)
   town = models.CharField(max_length=100, verbose_name = _("City"), blank=True)
   state = models.CharField(max_length=100, verbose_name = _("State"), blank=True)
   country = models.CharField(max_length=2, choices=[(x[0], x[3]) for x in COUNTRIES], verbose_name = _("Country"), blank=True)

   class Meta:
      app_label = "crm"
      verbose_name = _('Postal Address')
      verbose_name_plural = _('Postal Address')

class PhoneAddress(models.Model):
   phone = models.CharField(max_length=20, verbose_name = _("Phone Number"))

   class Meta:
      app_label = "crm"
      verbose_name = _('Phone Address')
      verbose_name_plural = _('Phone Address')

class EmailAddress(models.Model):
   email = models.EmailField(max_length=200, verbose_name = _("Email Address"))

   class Meta:
      app_label = "crm"
      verbose_name = _('Email Address')
      verbose_name_plural = _('Email Address')

class Contact(models.Model):
   name = models.CharField(max_length=300, verbose_name = _("Name"))
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"))
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Last modified by"), editable=True)

   class Meta:
      app_label = "crm"
      verbose_name = _('Contact')
      verbose_name_plural = _('Contact')

class Customer(Contact):
   class Meta:
      app_label = "crm"
      verbose_name = _('Customer')
      verbose_name_plural = _('Customers')

   def __unicode__(self):
      return str(self.id) + ' ' + self.name

class Distributor(Contact):
   class Meta:
      app_label = "crm"
      verbose_name = _('Distributor')
      verbose_name_plural = _('Distributors')

   def __unicode__(self):
      return str(self.id) + ' ' + self.name

class ShipmentPartner(Contact):
   class Meta:
      app_label = "crm"
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
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name = _("Last modified by"), related_name="db_contractlstmodified")

   class Meta:
      app_label = "crm"
      verbose_name = _('Contract')
      verbose_name_plural = _('Contracts')

   def __unicode__(self):
      return str(self.id)

class PurchaseOrder(models.Model):
   contract = models.ForeignKey(Contract, verbose_name = _("Contract"))
   externalReference = models.CharField(verbose_name = _("External Reference"), max_length=100, blank=True)
   distributor = models.ForeignKey(Distributor, verbose_name = _("Distributor"))
   state = models.CharField(max_length=1, choices=PURCHASEORDERSTATES)
   staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Staff"), related_name="db_relpostaff")
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"))
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name = _("Last modified by"), related_name="db_polstmodified")

   class Meta:
      app_label = "crm"
      verbose_name = _('Purchase Order')
      verbose_name_plural = _('Purchase Order')

   def __unicode__(self):
      return str(self.contract.id) + " " + str(self.id)

class SalesContract(models.Model):
   contract = models.ForeignKey(Contract)
   externalReference = models.CharField(verbose_name = _("External Reference"), max_length=100, blank=True)
   discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = _("Discount"), blank=True, null=True)
   description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True)
   lastPricingDate = models.DateField(verbose_name = _("Last Pricing Date"), blank=True, null=True)
   lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Price"), blank=True, null=True)
   customer = models.ForeignKey(Customer, verbose_name = _("Customer"))
   staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name = _("Staff"), related_name="db_relscstaff")
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"))
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name = _("Last modified by"), related_name="db_lstscmodified")
      
   def recalculatePrices(self, pricingDate):
      self.lastCalculatedPrice = self.getPrice(pricingDate)
      self.lastPricingDate = pricingDate
      self.save()
   
   def getPrice(self, pricingDate):
      price = 0
      try:
         positions = SalesContractPosition.objects.filter(contract=self.id)
         if type(positions) == SalesContractPosition:
            if type(self.discount) == Decimal:
               price = positions.recalculatePrices(pricingDate)*self.discount
            else:
               price = positions.recalculatePrices(pricingDate)
         else:
            for position in positions:
               if type(self.discount) == Decimal:
                  price += position.recalculatePrices(pricingDate)*self.discount
               else:
                  price += position.recalculatePrices(pricingDate)
         return price
      except Quote.DoesNotExist:  
         return 0

   class Meta:
      app_label = "crm"
      verbose_name = _('Sales Contract')
      verbose_name_plural = _('Sales Contracts')

   def __unicode__(self):
      return str(self.contract.id) + " " + str(self.id)

class Quote(SalesContract):
   validuntil = models.DateField(verbose_name = _("Valid until"))
   state = models.CharField(max_length=1, choices=QUOTESTATES)

# TODO:   def createSalesOrderPDF():
# TODO:   def createQuotePDF():
#      objectsToGenerateXML = list(Quote.objects.filter(id=self.id)) + list(Position.objects.filter(contract=self.id))
#      destinationFile = "/home/aaron/quote.xml"
#      file = open(destinationFile, 'w')
#      data = serializers.serialize('xml', objectsToGenerateXML)
#      file.write(data)
#      file.close()

   def createInvoice(self):
      invoice = Invoice()
      invoice.contact = self.contract
      invoice.description = self.description
      invoice.discount = self.discount
      invoice.customer = self.customer
      invoice.state = 'C'
      invoice.derivatedFromQuote = self
      invoice.payableuntil = date.today().__str__()
# TODO: today is not correct it has to be replaced
      invoice.save()
      try:
         quotePositions = SalesContractPosition.objects.filter(contract=self.id)
         if type(quotePositions) == SalesContractPosition:
            invoicePosition = Position()
            invoicePosition = copy.copy(quotePositions)
            invoicePosition.pk = None
            invoicePosition.contract = invoice
            invoicePosition.save()
         else:
            for quotePosition in quotePositions:
               invoicePosition = Position()
               invoicePosition = copy.copy(quotePosition)
               invoicePosition.pk = None
               invoicePosition.contract = invoice
               invoicePosition.save()
         return
      except Quote.DoesNotExist:  
         return

   def createPDF(self):
     XMLSerializer = serializers.get_serializer("xml")
     xml_serializer = XMLSerializer()
     out = open("/tmp/quote_"+str(self.id)+".xml", "w")
     objectsToSerialize = list(Quote.objects.filter(id=self.id)) + list(SalesContract.objects.filter(id=self.id)) + list(Contact.objects.filter(id=self.customer.id))
     objectsToSerialize += list(auth.models.User.objects.filter(id=self.staff.id))
     objectsToSerialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
     for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
         objectsToSerialize += list(PostalAddress.objects.filter(id=address.id))
     for position in list(SalesContractPosition.objects.filter(contract=self.id)):
         objectsToSerialize += list(Position.objects.filter(id=position.id))
     xml_serializer.serialize(objectsToSerialize, stream=out, indent=3)
     styledoc = libxml2.parseFile("/var/www/koalixcrm/quote.xsl")
     style = libxslt.parseStylesheetDoc(styledoc)
     doc = libxml2.parseFile("/tmp/quote_"+str(self.id)+".xml")
     result = style.applyStylesheet(doc, None)
     style.saveResultToFilename("/tmp/quote_"+str(self.id)+"_fop.xml", result, 0)
     style.freeStylesheet()
     doc.freeDoc()
     result.freeDoc()


   class Meta:
      app_label = "crm"
      verbose_name = _('Quote')
      verbose_name_plural = _('Quotes')

class Invoice(SalesContract):
   payableuntil = models.DateField(verbose_name = _("To pay until"))
   derivatedFromQuote = models.ForeignKey(Quote, blank=True, null=True)
   paymentBankReference = models.CharField(verbose_name = _("Payment Bank Reference"), max_length=100, blank=True)
   state = models.CharField(max_length=1, choices=INVOICESTATES)

# TODO:   def printDeliveryOrder():

   class Meta:
      app_label = "crm"
      verbose_name = _('Invoice')
      verbose_name_plural = _('Invoices') 

class Unit(models.Model):
   description = models.CharField(verbose_name = _("Description"), max_length=100)
   shortName = models.CharField(verbose_name = _("Displayed Name After Quantity"), max_length=100)
   isAFractionOf = models.ForeignKey('self', blank=True, null=True, verbose_name = _("Is A Fraction Of"))
   fractionFactorToNextHigherUnit = models.IntegerField(verbose_name = _("Factor Between This And Next Higher Unit"), blank=True, null=True)

   def __unicode__(self):
      return  self.shortName

   class Meta:
      app_label = "crm"
      verbose_name = _('Unit')
      verbose_name_plural = _('Units') 
      
	
class Product(models.Model):
   description = models.TextField(verbose_name = _("Description"), blank=True) 
   title = models.CharField(verbose_name = _("Title"), max_length=200)
   productNumber = models.IntegerField(verbose_name = _("Product Number"))
   dateofcreation = models.DateTimeField(verbose_name = _("Created at"))
   lastmodification = models.DateTimeField(verbose_name = _("Last modified"), blank=True, null=True)
   lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, verbose_name = _("Last modified by"))
   unit = models.ForeignKey(Unit, blank=False)

   def getPrice(self, date):
      price = Price.objects.get(product=self.id)
      # TODO: Filter for date 
      return price;

   def __unicode__(self):
      return str(self.productNumber) + ' ' + self.title

   class Meta:
      app_label = "crm"
      verbose_name = _('Product')
      verbose_name_plural = _('Products')

class Price(models.Model):
   product = models.ForeignKey(Product, verbose_name = _("Product"))
   price = models.DecimalField(max_digits=17, decimal_places=2, verbose_name = _("Price"))
   validfrom = models.DateField(verbose_name = _("Valid from"))
   validuntil = models.DateField(verbose_name = _("Valid until"))

   class Meta:
      app_label = "crm"
      verbose_name = _('Price')
      verbose_name_plural = _('Prices')

class Position(models.Model):
   positionNumber = models.IntegerField(verbose_name = _("Position Number"))
   quantity = models.IntegerField(verbose_name = _("Quantity"))
   description = models.TextField(verbose_name = _("Description"), blank=True, null=True)
   discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = _("Discount"), blank=True, null=True)
   product = models.ForeignKey(Product, verbose_name = _("Product"), blank=True, null=True)
   sentOn = models.DateField(verbose_name = _("Shipment on"), blank=True, null=True)
   shipmentPartner = models.ForeignKey(ShipmentPartner, verbose_name = _("Shipment Partner"), blank=True, null=True)
   shipmentID = models.CharField(max_length=100, verbose_name = _("Shipment ID"), blank=True, null=True)
   overwriteProductPrice = models.BooleanField(verbose_name=_('Overwrite Product Price'))
   positionPricePerUnit = models.DecimalField(max_digits=17, decimal_places=2)
   lastPricingDate = models.DateField(verbose_name = _("Last Pricing Date"), blank=True, null=True)
   lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Price"), blank=True, null=True)
   lastReferedPrice = models.ForeignKey(Price, blank=True, null=True)

   def recalculatePrices(self, pricingDate):
      if self.overwriteProductPrice :
         if type(self.discount) == Decimal:
            self.lastCalculatedPrice = self.positionPricePerUnit*self.quantity*self.discount
         else:
            self.lastCalculatedPrice = self.positionPricePerUnit*self.quantity
      else:
         self.lastReferedPrice = self.product.getPrice(pricingDate)
         if type(self.discount) == Decimal:
            self.lastCalculatedPrice = self.lastReferedPrice.price*self.quantity*self.discount
         else:
            self.lastCalculatedPrice = self.lastReferedPrice.price*self.quantity
      self.lastPricingDate = pricingDate
      self.save()
      return self.lastCalculatedPrice

   class Meta:
      app_label = "crm"
      verbose_name = _('Position')
      verbose_name_plural = _('Positions')

class SalesContractPosition(Position):
   contract = models.ForeignKey(SalesContract, verbose_name = _("Contract"))

class PurchaseOrderPosition(Position):
   contract = models.ForeignKey(PurchaseOrder, verbose_name = _("Contract"))

class PhoneAddressForContact(PhoneAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
   person = models.ForeignKey(Contact)

   class Meta:
      app_label = "crm"
      verbose_name = _('Phone Address For Contact')
      verbose_name_plural = _('Phone Address For Contact')

   def __unicode__(self):
      return str(self.phone)

class EmailAddressForContact(EmailAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
   person = models.ForeignKey(Contact)

   class Meta:
      app_label = "crm"
      verbose_name = _('Email Address For Contact')
      verbose_name_plural = _('Email Address For Contact')

   def __unicode__(self):
      return str(self.email)

class PostalAddressForContact(PostalAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
   person = models.ForeignKey(Contact)

   class Meta:
      app_label = "crm"
      verbose_name = _('Postal Address For Contact')
      verbose_name_plural = _('Postal Address For Contact')

   def __unicode__(self):
      return self.prename + ' ' + self.name + ' ' + self.addressline1
   
class PostalAddressForContract(PostalAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(Contract)

   class Meta:
      app_label = "crm"
      verbose_name = _('Postal Address For Contracts')
      verbose_name_plural = _('Postal Address For Contracts')

   def __unicode__(self):
      return self.prename + ' ' + self.name + ' ' + self.addressline1
   
class PostalAddressForPurchaseOrder(PostalAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(PurchaseOrder)

   class Meta:
      app_label = "crm"
      verbose_name = _('Postal Address For Contracts')
      verbose_name_plural = _('Postal Address For Contracts')

   def __unicode__(self):
      return self.prename + ' ' + self.name + ' ' + self.addressline1
   
class PostalAddressForSalesContract(PostalAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(SalesContract)

   class Meta:
      app_label = "crm"
      verbose_name = _('Postal Address For Contracts')
      verbose_name_plural = _('Postal Address For Contracts')

   def __unicode__(self):
      return self.prename + ' ' + self.name + ' ' + self.addressline1

class PhoneAddressForContract(PhoneAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(Contract)

   class Meta:
      app_label = "crm"
      verbose_name = _('Phone Address For Contracts')
      verbose_name_plural = _('Phone Address For Contracts')

   def __unicode__(self):
      return str(self.phone)

class PhoneAddressForSalesContract(PhoneAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(SalesContract)

   class Meta:
      app_label = "crm"
      verbose_name = _('Phone Address For Contracts')
      verbose_name_plural = _('Phone Address For Contracts')

   def __unicode__(self):
      return str(self.phone)

class PhoneAddressForPurchaseOrder(PhoneAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCONTRACT)
   contract = models.ForeignKey(PurchaseOrder)

   class Meta:
      app_label = "crm"
      verbose_name = _('Phone Address For Contracts')
      verbose_name_plural = _('Phone Address For Contracts')

   def __unicode__(self):
      return str(self.phone)

class EmailAddressForContract(EmailAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCONTRACT) 
   contract = models.ForeignKey(Contract)

   class Meta:
      app_label = "crm"
      verbose_name = _('Email Address For Contracts')
      verbose_name_plural = _('Email Address For Contracts')

   def __unicode__(self):
      return str(self.email)

class EmailAddressForSalesContract(EmailAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCONTRACT) 
   contract = models.ForeignKey(SalesContract)

   class Meta:
      app_label = "crm"
      verbose_name = _('Email Address For Contracts')
      verbose_name_plural = _('Email Address For Contracts')

   def __unicode__(self):
      return str(self.email)

class EmailAddressForPurchaseOrder(EmailAddress):
   purpose = models.CharField(max_length=1, choices=PURPOSESADDRESSINCONTRACT) 
   contract = models.ForeignKey(PurchaseOrder)

   class Meta:
      app_label = "crm"
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