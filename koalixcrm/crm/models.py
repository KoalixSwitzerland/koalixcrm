# -*- coding: utf-8 -*-

from datetime import *
from decimal import Decimal
from subprocess import *

from django.conf import settings
from django.contrib import auth
from django.core import serializers
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.country import *
from koalixcrm.crm.const.postaladdressprefix import *
from koalixcrm.crm.const.purpose import *
from koalixcrm.crm.const.status import *
from koalixcrm.crm.exceptions import OpenInterestAccountMissing
from koalixcrm.crm.exceptions import TemplateSetMissing
from koalixcrm.crm.exceptions import UserExtensionMissing
from koalixcrm.globalSupportFunctions import xstr
from koalixcrm import accounting
from koalixcrm import djangoUserExtension
from lxml import etree


class Currency(models.Model):
    description = models.CharField(verbose_name=_("Description"), max_length=100)
    shortName = models.CharField(verbose_name=_("Displayed Name After Price In The Position"), max_length=3)
    rounding = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Rounding"), blank=True, null=True)

    def __str__(self):
        return self.shortName

    class Meta:
        app_label = "crm"
        verbose_name = _('Currency')
        verbose_name_plural = _('Currency')


class PostalAddress(models.Model):
    prefix = models.CharField(max_length=1, choices=POSTALADDRESSPREFIX, verbose_name=_("Prefix"), blank=True,
                              null=True)
    name = models.CharField(max_length=100, verbose_name=_("Name"), blank=True, null=True)
    prename = models.CharField(max_length=100, verbose_name=_("Prename"), blank=True, null=True)
    addressline1 = models.CharField(max_length=200, verbose_name=_("Addressline 1"), blank=True, null=True)
    addressline2 = models.CharField(max_length=200, verbose_name=_("Addressline 2"), blank=True, null=True)
    addressline3 = models.CharField(max_length=200, verbose_name=_("Addressline 3"), blank=True, null=True)
    addressline4 = models.CharField(max_length=200, verbose_name=_("Addressline 4"), blank=True, null=True)
    zipcode = models.IntegerField(verbose_name=_("Zipcode"), blank=True, null=True)
    town = models.CharField(max_length=100, verbose_name=_("City"), blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name=_("State"), blank=True, null=True)
    country = models.CharField(max_length=2, choices=[(x[0], x[3]) for x in COUNTRIES], verbose_name=_("Country"),
                               blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address')
        verbose_name_plural = _('Postal Address')


class PhoneAddress(models.Model):
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address')
        verbose_name_plural = _('Phone Address')


class EmailAddress(models.Model):
    email = models.EmailField(max_length=200, verbose_name=_("Email Address"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address')
        verbose_name_plural = _('Email Address')


class Contact(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                                       verbose_name=_("Last modified by"), editable=True)

    class Meta:
        app_label = "crm"
        verbose_name = _('Contact')
        verbose_name_plural = _('Contact')


class CustomerBillingCycle(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    timeToPaymentDate = models.IntegerField(verbose_name=_("Days To Payment Date"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer Billing Cycle')
        verbose_name_plural = _('Customer Billing Cycle')

    def __str__(self):
        return str(self.id) + ' ' + self.name


class CustomerGroup(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id) + ' ' + self.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer Group')
        verbose_name_plural = _('Customer Groups')


class Customer(Contact):
    defaultCustomerBillingCycle = models.ForeignKey('CustomerBillingCycle', verbose_name=_('Default Billing Cycle'))
    ismemberof = models.ManyToManyField(CustomerGroup, verbose_name=_('Is member of'), blank=True)

    def createContract(self, request):
        contract = Contract()
        contract.defaultcustomer = self
        contract.defaultcurrency = djangoUserExtension.models.UserExtension.objects.filter(user=request.user.id)[
            0].defaultCurrency
        contract.lastmodifiedby = request.user
        contract.staff = request.user
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
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return str(self.id) + ' ' + self.name


class Supplier(Contact):
    offersShipmentToCustomers = models.BooleanField(verbose_name=_("Offers Shipment to Customer"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Supplier')
        verbose_name_plural = _('Supplier')

    def __str__(self):
        return str(self.id) + ' ' + self.name


class Contract(models.Model):
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relcontractstaff", null=True)
    description = models.TextField(verbose_name=_("Description"))
    defaultcustomer = models.ForeignKey(Customer, verbose_name=_("Default Customer"), null=True, blank=True)
    defaultSupplier = models.ForeignKey(Supplier, verbose_name=_("Default Supplier"), null=True, blank=True)
    defaultcurrency = models.ForeignKey(Currency, verbose_name=_("Default Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_contractlstmodified")

    class Meta:
        app_label = "crm"
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    def createInvoice(self):
        invoice = Invoice()
        invoice.contract = self
        invoice.discount = 0
        invoice.staff = self.staff
        invoice.customer = self.defaultcustomer
        invoice.status = 'C'
        invoice.currency = self.defaultcurrency
        invoice.payableuntil = date.today() + timedelta(
            days=self.defaultcustomer.defaultCustomerBillingCycle.timeToPaymentDate)
        invoice.dateofcreation = date.today().__str__()
        invoice.save()
        return invoice

    def createQuote(self):
        quote = Quote()
        quote.contract = self
        quote.discount = 0
        quote.staff = self.staff
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
        purchaseorder.supplier = self.defaultSupplier
        purchaseorder.status = 'C'
        purchaseorder.dateofcreation = date.today().__str__()
        # TODO: today is not correct it has to be replaced
        purchaseorder.save()
        return purchaseorder

    def __str__(self):
        return _("Contract") + " " + str(self.id)


class PurchaseOrder(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=_("Contract"))
    externalReference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, verbose_name=_("Supplier"))
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2,
                                              verbose_name=_("Last Calculted Price With Tax"), blank=True, null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"),
                                            blank=True, null=True)
    status = models.CharField(max_length=1, choices=PURCHASEORDERSTATUS)
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relpostaff", null=True)
    currency = models.ForeignKey(Currency, verbose_name=_("Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_polstmodified")

    def recalculatePrices(self, pricingDate):
        price = 0
        tax = 0
        try:
            positions = PurchaseOrderPosition.objects.filter(contract=self.id)
            if type(positions) == PurchaseOrderPosition:
                if type(self.discount) == Decimal:
                    price = int(positions.recalculatePrices(pricingDate, self.customer, self.currency) * (
                    1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    tax = int(positions.recalculateTax(self.currency) * (
                    1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                else:
                    price = positions.recalculatePrices(pricingDate, self.customer, self.currency)
                    tax = positions.recalculateTax(self.currency)
            else:
                for position in positions:
                    if type(self.discount) == Decimal:
                        price += int(position.recalculatePrices(pricingDate, self.customer, self.currency) * (
                        1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                        tax += int(position.recalculateTax(self.currency) * (
                        1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    else:
                        price += position.recalculatePrices(pricingDate, self.customer, self.currency)
                        tax += position.recalculateTax(self.currency)
            self.lastCalculatedPrice = price
            self.lastCalculatedTax = tax
            self.lastPricingDate = pricingDate
            self.save()
            return 1
        except Quote.DoesNotExist as e:
            print("ERROR " + e.__str__())
            print("Der Fehler trat beim File: " + self.sourcefile + " / Cell: " + listOfLines[0][
                                                                                  listOfLines[0].find("cell ") + 4:
                                                                                  listOfLines[0].find(
                                                                                      "(cellType ") - 1] + " auf!")
            exit()
            return 0

    def createPDF(self, whatToExport):
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        out = open(settings.PDF_OUTPUT_ROOT + "purchaseorder_" + str(self.id) + ".xml", "wb")
        objectsToSerialize = list(PurchaseOrder.objects.filter(id=self.id))
        objectsToSerialize += list(Contact.objects.filter(id=self.supplier.id))
        objectsToSerialize += list(Currency.objects.filter(id=self.currency.id))
        objectsToSerialize += list(PurchaseOrderPosition.objects.filter(contract=self.id))
        for position in list(PurchaseOrderPosition.objects.filter(contract=self.id)):
            objectsToSerialize += list(Position.objects.filter(id=position.id))
            objectsToSerialize += list(Product.objects.filter(id=position.product.id))
            objectsToSerialize += list(Unit.objects.filter(id=position.unit.id))
        objectsToSerialize += list(auth.models.User.objects.filter(id=self.staff.id))
        userExtension = djangoUserExtension.models.UserExtension.objects.filter(user=self.staff.id)
        if len(userExtension) == 0:
            raise UserExtensionMissing(_("During PurchaseOrder PDF Export"))
        phoneAddress = djangoUserExtension.models.UserExtensionPhoneAddress.objects.filter(
            userExtension=userExtension[0].id)
        objectsToSerialize += list(userExtension)
        objectsToSerialize += list(phoneAddress)
        templateset = djangoUserExtension.models.TemplateSet.objects.filter(id=userExtension[0].defaultTemplateSet.id)
        if len(templateset) == 0:
            raise TemplateSetMissing(_("During PurchaseOrder PDF Export"))
        objectsToSerialize += list(templateset)
        objectsToSerialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objectsToSerialize += list(PostalAddressForContact.objects.filter(person=self.supplier.id))
        for address in list(PostalAddressForContact.objects.filter(person=self.supplier.id)):
            objectsToSerialize += list(PostalAddress.objects.filter(id=address.id))
        xml_serializer.serialize(objectsToSerialize, stream=out, indent=3)
        out.close()
        check_output(['/usr/bin/fop', '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path_full, '-xml',
                      settings.PDF_OUTPUT_ROOT + 'purchaseorder_' + str(self.id) + '.xml', '-xsl',
                      userExtension[0].defaultTemplateSet.purchaseorderXSLFile.xslfile.path_full, '-pdf',
                      settings.PDF_OUTPUT_ROOT + 'purchaseorder_' + str(self.id) + '.pdf'], stderr=STDOUT)
        return settings.PDF_OUTPUT_ROOT + "purchaseorder_" + str(self.id) + ".pdf"

    class Meta:
        app_label = "crm"
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Order')

    def __str__(self):
        return _("Purchase Order") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)


class SalesContract(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=_('Contract'))
    externalReference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2,
                                              verbose_name=_("Last Calculted Price With Tax"), blank=True, null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"),
                                            blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"))
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relscstaff", null=True)
    currency = models.ForeignKey(Currency, verbose_name=_("Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_lstscmodified", null=True,
                                       blank="True")

    def recalculatePrices(self, pricingDate):
        price = 0
        tax = 0
        try:
            positions = SalesContractPosition.objects.filter(contract=self.id)
            if type(positions) == SalesContractPosition:
                if type(self.discount) == Decimal:
                    price = int(positions.recalculatePrices(pricingDate, self.customer, selof.currency) * (
                    1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    tax = int(positions.recalculateTax(self.currency) * (
                    1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                else:
                    price = positions.recalculatePrices(pricingDate, self.customer, self.currency)
                    tax = positions.recalculateTax(self.currency)
            else:
                for position in positions:
                    price += position.recalculatePrices(pricingDate, self.customer, self.currency)
                    tax += position.recalculateTax(self.currency)
                if type(self.discount) == Decimal:
                    price = int(price * (1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    tax = int(tax * (1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding

            self.lastCalculatedPrice = price
            self.lastCalculatedTax = tax
            self.lastPricingDate = pricingDate
            self.save()
            return 1
        except Quote.DoesNotExist:
            return 0

    class Meta:
        app_label = "crm"
        verbose_name = _('Sales Contract')
        verbose_name_plural = _('Sales Contracts')

    def __str__(self):
        return _("Sales Contract") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)


class Quote(SalesContract):
    validuntil = models.DateField(verbose_name=_("Valid until"))
    status = models.CharField(max_length=1, choices=QUOTESTATUS, verbose_name=_('Status'))

    def createInvoice(self):
        invoice = Invoice()
        invoice.contract = self.contract
        invoice.description = self.description
        invoice.discount = self.discount
        invoice.customer = self.customer
        invoice.staff = self.staff
        invoice.status = 'C'
        invoice.derivatedFromQuote = self
        invoice.currency = self.currency
        invoice.payableuntil = date.today() + timedelta(
            days=self.customer.defaultCustomerBillingCycle.timeToPaymentDate)
        invoice.dateofcreation = date.today().__str__()
        invoice.customerBillingCycle = self.customer.defaultCustomerBillingCycle
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
                invoicePosition.supplier = quotePosition.supplier
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

    def createPDF(self, whatToExport):
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        out = open(settings.PDF_OUTPUT_ROOT + "quote_" + str(self.id) + ".xml", "wb")
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
        userExtension = djangoUserExtension.models.UserExtension.objects.filter(user=self.staff.id)
        if (len(userExtension) == 0):
            raise UserExtensionMissing(_("During Quote PDF Export"))
        phoneAddress = djangoUserExtension.models.UserExtensionPhoneAddress.objects.filter(
            userExtension=userExtension[0].id)
        objectsToSerialize += list(userExtension)
        objectsToSerialize += list(PhoneAddress.objects.filter(id=phoneAddress[0].id))
        templateset = djangoUserExtension.models.TemplateSet.objects.filter(id=userExtension[0].defaultTemplateSet.id)
        if (len(templateset) == 0):
            raise TemplateSetMissing(_("During Quote PDF Export"))
        objectsToSerialize += list(templateset)
        objectsToSerialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objectsToSerialize += list(PostalAddressForContact.objects.filter(person=self.customer.id))
        for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
            objectsToSerialize += list(PostalAddress.objects.filter(id=address.id))
        xml_serializer.serialize(objectsToSerialize, stream=out, indent=3)
        out.close()
        xml = etree.parse(settings.PDF_OUTPUT_ROOT + "quote_" + str(self.id) + ".xml")
        rootelement = xml.getroot()
        filebrowserdirectory = etree.SubElement(rootelement, "filebrowserdirectory")
        filebrowserdirectory.text = settings.FILEBROWSER_DIRECTORY
        xml.write(settings.PDF_OUTPUT_ROOT + "quote_" + str(self.id) + ".xml")
        if (whatToExport == "quote"):
            check_output(
                ['/usr/bin/fop', '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path_full, '-xml',
                 settings.PDF_OUTPUT_ROOT + 'quote_' + str(self.id) + '.xml', '-xsl',
                 userExtension[0].defaultTemplateSet.quoteXSLFile.xslfile.path_full, '-pdf',
                 settings.PDF_OUTPUT_ROOT + 'quote_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "quote_" + str(self.id) + ".pdf"
        else:
            check_output(
                ['/usr/bin/fop', '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path_full, '-xml',
                 settings.PDF_OUTPUT_ROOT + 'quote_' + str(self.id) + '.xml', '-xsl',
                 userExtension[0].defaultTemplateSet.purchaseconfirmationXSLFile.xslfile.path_full, '-pdf',
                 settings.PDF_OUTPUT_ROOT + 'purchaseconfirmation_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "purchaseconfirmation_" + str(self.id) + ".pdf"

    def __str__(self):
        return _("Quote") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')


class Invoice(SalesContract):
    payableuntil = models.DateField(verbose_name=_("To pay until"))
    derivatedFromQuote = models.ForeignKey(Quote, blank=True, null=True)
    paymentBankReference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                            null=True)
    status = models.CharField(max_length=1, choices=INVOICESTATUS)

    def registerinvoiceinaccounting(self, request):
        dictprices = dict()
        dicttax = dict()
        exists = False
        currentValidAccountingPeriod = accounting.models.AccountingPeriod.getCurrentValidAccountingPeriod()
        activaaccount = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        if len(activaaccount) == 0:
            raise OpenInterestAccountMissing(_("Please specify one open intrest account in the accounting"))
        for position in list(SalesContractPosition.objects.filter(contract=self.id)):
            profitaccount = position.product.accoutingProductCategorie.profitAccount
            dictprices[profitaccount] = position.lastCalculatedPrice
            dicttax[profitaccount] = position.lastCalculatedTax

        for booking in accounting.models.Booking.objects.filter(accountingPeriod=currentValidAccountingPeriod):
            if booking.bookingReference == self:
                raise InvoiceAlreadyRegistered()
        for profitaccount, amount in iter(dictprices.items()):
            booking = accounting.models.Booking()
            booking.toAccount = activaaccount[0]
            booking.fromAccount = profitaccount
            booking.bookingReference = self
            booking.accountingPeriod = currentValidAccountingPeriod
            booking.bookingDate = date.today().__str__()
            booking.staff = request.user
            booking.amount = amount
            booking.lastmodifiedby = request.user
            booking.save()

    def registerpaymentinaccounting(self, request, amount, paymentaccount):
        currentValidAccountingPeriod = accounting.models.AccountingPeriod.getCurrentValidAccountingPeriod()
        activaaccount = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        booking = accounting.models.Booking()
        booking.toAccount = paymentaccount
        booking.fromAccount = activaaccount[0]
        booking.bookingDate = date.today().__str__()
        booking.bookingReference = self
        booking.accountingPeriod = currentValidAccountingPeriod
        booking.amount = self.lastCalculatedPrice
        booking.staff = request.user
        booking.lastmodifiedby = request.user
        booking.save()

    def createPDF(self, whatToExport):
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        out = open(settings.PDF_OUTPUT_ROOT + "invoice_" + str(self.id) + ".xml", "wb")
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
        userExtension = djangoUserExtension.models.UserExtension.objects.filter(user=self.staff.id)
        if (len(userExtension) == 0):
            raise UserExtensionMissing(_("During Invoice PDF Export"))
        phoneAddress = djangoUserExtension.models.UserExtensionPhoneAddress.objects.filter(
            userExtension=userExtension[0].id)
        objectsToSerialize += list(userExtension)
        objectsToSerialize += list(PhoneAddress.objects.filter(id=phoneAddress[0].id))
        templateset = djangoUserExtension.models.TemplateSet.objects.filter(id=userExtension[0].defaultTemplateSet.id)
        if (len(templateset) == 0):
            raise TemplateSetMissing(_("During Invoice PDF Export"))
        objectsToSerialize += list(templateset)
        objectsToSerialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objectsToSerialize += list(PostalAddressForContact.objects.filter(person=self.customer.id))
        for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
            objectsToSerialize += list(PostalAddress.objects.filter(id=address.id))
        xml_serializer.serialize(objectsToSerialize, stream=out, indent=3)
        out.close()
        xml = etree.parse(settings.PDF_OUTPUT_ROOT + "invoice_" + str(self.id) + ".xml")
        rootelement = xml.getroot()
        filebrowserdirectory = etree.SubElement(rootelement, "filebrowserdirectory")
        filebrowserdirectory.text = settings.FILEBROWSER_DIRECTORY
        xml.write(settings.PDF_OUTPUT_ROOT + "invoice_" + str(self.id) + ".xml")
        if (whatToExport == "invoice"):
            check_output(
                ['/usr/bin/fop', '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path_full, '-xml',
                 settings.PDF_OUTPUT_ROOT + 'invoice_' + str(self.id) + '.xml', '-xsl',
                 userExtension[0].defaultTemplateSet.invoiceXSLFile.xslfile.path_full, '-pdf',
                 settings.PDF_OUTPUT_ROOT + 'invoice_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "invoice_" + str(self.id) + ".pdf"
        else:
            check_output(
                ['/usr/bin/fop', '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path_full, '-xml',
                 settings.PDF_OUTPUT_ROOT + 'invoice_' + str(self.id) + '.xml', '-xsl',
                 userExtension[0].defaultTemplateSet.deilveryorderXSLFile.xslfile.path_full, '-pdf',
                 settings.PDF_OUTPUT_ROOT + 'deliveryorder_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "deliveryorder_" + str(self.id) + ".pdf"

        #  TODO: def registerPayment(self, amount, registerpaymentinaccounting):

    def __str__(self):
        return _("Invoice") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


class Unit(models.Model):
    description = models.CharField(verbose_name=_("Description"), max_length=100)
    shortName = models.CharField(verbose_name=_("Displayed Name After Quantity In The Position"), max_length=3)
    isAFractionOf = models.ForeignKey('self', blank=True, null=True, verbose_name=_("Is A Fraction Of"))
    fractionFactorToNextHigherUnit = models.IntegerField(verbose_name=_("Factor Between This And Next Higher Unit"),
                                                         blank=True, null=True)

    def __str__(self):
        return self.shortName

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')


class Tax(models.Model):
    taxrate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Taxrate in Percentage"))
    name = models.CharField(verbose_name=_("Taxname"), max_length=100)
    accountActiva = models.ForeignKey('accounting.Account', verbose_name=_("Activa Account"),
                                      related_name="db_relaccountactiva", null=True, blank=True)
    accountPassiva = models.ForeignKey('accounting.Account', verbose_name=_("Passiva Account"),
                                       related_name="db_relaccountpassiva", null=True, blank=True)

    def getTaxRate(self):
        return self.taxrate;

    def __str__(self):
        return self.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')


class Product(models.Model):
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    productNumber = models.IntegerField(verbose_name=_("Product Number"))
    defaultunit = models.ForeignKey(Unit, verbose_name=_("Unit"))
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), null=True, blank="True")
    tax = models.ForeignKey(Tax, blank=False)
    accoutingProductCategorie = models.ForeignKey('accounting.ProductCategorie',
                                                  verbose_name=_("Accounting Product Categorie"), null=True,
                                                  blank="True")

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
                        if price.matchesDateUnitCustomerGroupCurrency(date, unit,
                                                                      customerGroupTransfrom.transform(customerGroup),
                                                                      currency):
                            validpriceslist.append(price.price * customerGroup.factor);
                        else:
                            for unitTransfrom in list(unitTransforms):
                                if price.matchesDateUnitCustomerGroupCurrency(date,
                                                                              unitTransfrom.transfrom(unit).transform(
                                                                                      unitTransfrom),
                                                                              customerGroupTransfrom.transform(
                                                                                      customerGroup), currency):
                                    validpriceslist.append(
                                        price.price * customerGroupTransform.factor * unitTransform.factor);
        if (len(validpriceslist) > 0):
            lowestprice = validpriceslist[0]
            for price in validpriceslist:
                if (price < lowestprice):
                    lowestprice = price
            return lowestprice
        else:
            raise Product.NoPriceFound(customer, unit, date, self)

    def getTaxRate(self):
        return self.tax.getTaxRate();

    def __str__(self):
        return str(self.productNumber) + ' ' + self.title

    class Meta:
        app_label = "crm"
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    class NoPriceFound(Exception):
        def __init__(self, customer, unit, date, product):
            self.customer = customer
            self.unit = unit
            self.date = date
            self.product = product
            return

        def __str__(self):
            return _("There is no Price for this product") + ": " + self.product.__str__() + _(
                "that matches the date") + ": " + self.date.__str__() + " ," + _(
                "customer") + ": " + self.customer.__str__() + _(" and unit") + ":" + self.unit.__str__()


class UnitTransform(models.Model):
    fromUnit = models.ForeignKey('Unit', verbose_name=_("From Unit"), related_name="db_reltransfromfromunit")
    toUnit = models.ForeignKey('Unit', verbose_name=_("To Unit"), related_name="db_reltransfromtounit")
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Unit"), blank=True, null=True)

    def transform(self, unit):
        if (self.fromUnit == unit):
            return self.toUnit
        else:
            return unit

    def __str__(self):
        return "From " + self.fromUnit.shortName + " to " + self.toUnit.shortName

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit Transfrom')
        verbose_name_plural = _('Unit Transfroms')


class CustomerGroupTransform(models.Model):
    fromCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name=_("From Unit"),
                                          related_name="db_reltransfromfromcustomergroup")
    toCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name=_("To Unit"),
                                        related_name="db_reltransfromtocustomergroup")
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Customer Group"), blank=True, null=True)

    def transform(self, customerGroup):
        if (self.fromCustomerGroup == customerGroup):
            return self.toCustomerGroup
        else:
            return unit

    def __str__(self):
        return "From " + self.fromCustomerGroup.name + " to " + self.toCustomerGroup.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer Group Price Transfrom')
        verbose_name_plural = _('Customer Group Price Transfroms')


class Price(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"))
    unit = models.ForeignKey(Unit, blank=False, verbose_name=_("Unit"))
    currency = models.ForeignKey(Currency, blank=False, null=False, verbose_name=('Currency'))
    customerGroup = models.ForeignKey(CustomerGroup, blank=True, null=True, verbose_name=_("Customer Group"))
    price = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Price Per Unit"))
    validfrom = models.DateField(verbose_name=_("Valid from"), blank=True, null=True)
    validuntil = models.DateField(verbose_name=_("Valid until"), blank=True, null=True)

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
                if ((date - self.validuntil).days < 0) & (unit == self.unit) & (self.customerGroup == customerGroup) & (
                    self.currency == currency):
                    return 1
        elif self.validuntil == None:
            if self.customerGroup == None:
                if ((self.validfrom - date).days < 0) & (unit == self.unit) & (self.currency == currency):
                    return 1
            else:
                if ((self.validfrom - date).days < 0) & (unit == self.unit) & (self.customerGroup == customerGroup) & (
                    self.currency == currency):
                    return 1
        elif self.customerGroup == None:
            if ((self.validfrom - date).days < 0) & (self.validuntil == None) & (unit == self.unit) & (
                self.customerGroup == None) & (self.currency == currency):
                return 1
        else:
            if ((self.validfrom - date).days < 0) & ((date - self.validuntil).days < 0) & (unit == self.unit) & (
                self.customerGroup == customerGroup) & (self.currency == currency):
                return 1

    class Meta:
        app_label = "crm"
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')


class Position(models.Model):
    positionNumber = models.IntegerField(verbose_name=_("Position Number"))
    quantity = models.DecimalField(verbose_name=_("Quantity"), decimal_places=3, max_digits=10)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=_("Product"), blank=True, null=True)
    unit = models.ForeignKey(Unit, verbose_name=_("Unit"), blank=True, null=True)
    sentOn = models.DateField(verbose_name=_("Shipment on"), blank=True, null=True)
    supplier = models.ForeignKey(Supplier, verbose_name=_("Shipment Supplier"),
                                 limit_choices_to={'offersShipmentToCustomers': True}, blank=True, null=True)
    shipmentID = models.CharField(max_length=100, verbose_name=_("Shipment ID"), blank=True, null=True)
    overwriteProductPrice = models.BooleanField(verbose_name=_('Overwrite Product Price'))
    positionPricePerUnit = models.DecimalField(verbose_name=_("Price Per Unit"), max_digits=17, decimal_places=2,
                                               blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Price"),
                                              blank=True, null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"),
                                            blank=True, null=True)

    def recalculatePrices(self, pricingDate, customer, currency):
        if self.overwriteProductPrice == False:
            self.positionPricePerUnit = self.product.getPrice(pricingDate, self.unit, customer, currency)
        if type(self.discount) == Decimal:
            self.lastCalculatedPrice = int(self.positionPricePerUnit * self.quantity * (
            1 - self.discount / 100) / currency.rounding) * currency.rounding
        else:
            self.lastCalculatedPrice = self.positionPricePerUnit * self.quantity
        self.lastPricingDate = pricingDate
        self.save()
        return self.lastCalculatedPrice

    def recalculateTax(self, currency):
        if type(self.discount) == Decimal:
            self.lastCalculatedTax = int(self.product.getTaxRate() / 100 * self.positionPricePerUnit * self.quantity * (
            1 - self.discount / 100) / currency.rounding) * currency.rounding
        else:
            self.lastCalculatedTax = self.product.getTaxRate() / 100 * self.positionPricePerUnit * self.quantity
        self.save()
        return self.lastCalculatedTax

    def __str__(self):
        return _("Position") + ": " + str(self.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')


class SalesContractPosition(Position):
    contract = models.ForeignKey(SalesContract, verbose_name=_("Contract"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Salescontract Position')
        verbose_name_plural = _('Salescontract Positions')

    def __str__(self):
        return _("Salescontract Position") + ": " + str(self.id)


class PurchaseOrderPosition(Position):
    contract = models.ForeignKey(PurchaseOrder, verbose_name=_("Contract"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Purchaseorder Position')
        verbose_name_plural = _('Purchaseorder Positions')

    def __str__(self):
        return _("Purchaseorder Position") + ": " + str(self.id)


class PhoneAddressForContact(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contact')
        verbose_name_plural = _('Phone Address For Contact')

    def __str__(self):
        return str(self.phone)


class EmailAddressForContact(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contact')
        verbose_name_plural = _('Email Address For Contact')

    def __str__(self):
        return str(self.email)


class PostalAddressForContact(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contact')
        verbose_name_plural = _('Postal Address For Contact')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class PostalAddressForContract(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(Contract)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contracts')
        verbose_name_plural = _('Postal Address For Contracts')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class PostalAddressForPurchaseOrder(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(PurchaseOrder)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contracts')
        verbose_name_plural = _('Postal Address For Contracts')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class PostalAddressForSalesContract(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(SalesContract)

    class Meta:
        app_label = "crm"
        verbose_name = _('Postal Address For Contracts')
        verbose_name_plural = _('Postal Address For Contracts')

    def __str__(self):
        return xstr(self.prename) + ' ' + xstr(self.name) + ' ' + xstr(self.addressline1)


class PhoneAddressForContract(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(Contract)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contracts')
        verbose_name_plural = _('Phone Address For Contracts')

    def __str__(self):
        return str(self.phone)


class PhoneAddressForSalesContract(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(SalesContract)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contracts')
        verbose_name_plural = _('Phone Address For Contracts')

    def __str__(self):
        return str(self.phone)


class PhoneAddressForPurchaseOrder(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(PurchaseOrder)

    class Meta:
        app_label = "crm"
        verbose_name = _('Phone Address For Contracts')
        verbose_name_plural = _('Phone Address For Contracts')

    def __str__(self):
        return str(self.phone)


class EmailAddressForContract(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(Contract)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contracts')
        verbose_name_plural = _('Email Address For Contracts')

    def __str__(self):
        return str(self.email)


class EmailAddressForSalesContract(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(SalesContract)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contracts')
        verbose_name_plural = _('Email Address For Contracts')

    def __str__(self):
        return str(self.email)


class EmailAddressForPurchaseOrder(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(PurchaseOrder)

    class Meta:
        app_label = "crm"
        verbose_name = _('Email Address For Contracts')
        verbose_name_plural = _('Email Address For Contracts')

    def __str__(self):
        return str(self.email)
