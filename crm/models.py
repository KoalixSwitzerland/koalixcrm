# -*- coding: utf-8 -*-

from datetime import *
from decimal import Decimal
from subprocess import *
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as trans
from django.core import serializers
from django.contrib import auth
from xml import etree

from const.country import *
from const.postaladdressprefix import *
from const.purpose import *
from const.status import *
import djangoUserExtension
import accounting


class Currency(models.Model):
    description = models.CharField(verbose_name=trans("Description"), max_length=100)
    shortName = models.CharField(verbose_name=trans("Displayed Name After Price In The Position"), max_length=3)
    rounding = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=trans("Rounding"), blank=True,
                                   null=True)

    def __unicode__(self):
        return self.shortName

    class Meta:
        app_label = "crm"
        verbose_name = trans('Currency')
        verbose_name_plural = trans('Currency')


class PostalAddress(models.Model):
    prefix = models.CharField(max_length=1, choices=POSTALADDRESSPREFIX, verbose_name=trans("Prefix"), blank=True,
                              null=True)
    name = models.CharField(max_length=100, verbose_name=trans("Name"), blank=True, null=True)
    prename = models.CharField(max_length=100, verbose_name=trans("Prename"), blank=True, null=True)
    addressline1 = models.CharField(max_length=200, verbose_name=trans("Addressline 1"), blank=True, null=True)
    addressline2 = models.CharField(max_length=200, verbose_name=trans("Addressline 2"), blank=True, null=True)
    addressline3 = models.CharField(max_length=200, verbose_name=trans("Addressline 3"), blank=True, null=True)
    addressline4 = models.CharField(max_length=200, verbose_name=trans("Addressline 4"), blank=True, null=True)
    zipcode = models.IntegerField(verbose_name=trans("Zipcode"), blank=True, null=True)
    town = models.CharField(max_length=100, verbose_name=trans("City"), blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name=trans("State"), blank=True, null=True)
    country = models.CharField(max_length=2, choices=[(x[0], x[3]) for x in COUNTRIES], verbose_name=trans("Country"),
                               blank=True, null=True)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Postal Address')
        verbose_name_plural = trans('Postal Address')


class PhoneAddress(models.Model):
    phone = models.CharField(max_length=20, verbose_name=trans("Phone Number"))

    class Meta:
        app_label = "crm"
        verbose_name = trans('Phone Address')
        verbose_name_plural = trans('Phone Address')


class EmailAddress(models.Model):
    email = models.EmailField(max_length=200, verbose_name=trans("Email Address"))

    class Meta:
        app_label = "crm"
        verbose_name = trans('Email Address')
        verbose_name_plural = trans('Email Address')


class Contact(models.Model):
    name = models.CharField(max_length=300, verbose_name=trans("Name"))
    dateofcreation = models.DateTimeField(verbose_name=trans("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=trans("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True,
                                       verbose_name=trans("Last modified by"), editable=True)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Contact')
        verbose_name_plural = trans('Contact')


class CustomerBillingCycle(models.Model):
    name = models.CharField(max_length=300, verbose_name=trans("Name"))
    timeToPaymentDate = models.IntegerField(verbose_name=trans("Days To Payment Date"))

    class Meta:
        app_label = "crm"
        verbose_name = trans('Customer Billing Cycle')
        verbose_name_plural = trans('Customer Billing Cycle')

    def __unicode__(self):
        return str(self.id) + ' ' + self.name


class CustomerGroup(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return str(self.id) + ' ' + self.name

    class Meta:
        app_label = "crm"
        verbose_name = trans('Customer Group')
        verbose_name_plural = trans('Customer Groups')


class Customer(Contact):
    defaultCustomerBillingCycle = models.ForeignKey('CustomerBillingCycle', verbose_name=trans('Default Billing Cycle'))
    ismemberof = models.ManyToManyField(CustomerGroup, verbose_name=trans('Is member of'), blank=True, null=True)

    def create_contract(self, request):
        contract = Contract()
        contract.defaultcustomer = self
        contract.defaultcurrency = djangoUserExtension.models.UserExtension.objects.filter(user=request.user.id)[
            0].defaultCurrency
        contract.lastmodifiedby = request.user
        contract.staff = request.user
        contract.save()
        return contract

    def create_invoice(self, request):
        contract = self.create_contract(request)
        invoice = contract.create_invoice()
        return invoice

    def create_quote(self, request):
        contract = self.create_contract(request)
        quote = contract.create_quote()
        return quote

    def is_in_group(self, customer_group):
        for customerGroupMembership in self.ismemberof.all():
            if customerGroupMembership.id == customer_group.id:
                return 1
        return 0

    class Meta:
        app_label = "crm"
        verbose_name = trans('Customer')
        verbose_name_plural = trans('Customers')

    def __unicode__(self):
        return str(self.id) + ' ' + self.name


class Supplier(Contact):
    offersShipmentToCustomers = models.BooleanField(verbose_name=trans("Offers Shipment to Customer"), default=False)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Supplier')
        verbose_name_plural = trans('Supplier')

    def __unicode__(self):
        return str(self.id) + ' ' + self.name


class Contract(models.Model):
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=trans("Staff"),
                              related_name="db_relcontractstaff", null=True)
    description = models.TextField(verbose_name=trans("Description"))
    defaultcustomer = models.ForeignKey(Customer, verbose_name=trans("Default Customer"), null=True, blank=True)
    defaultSupplier = models.ForeignKey(Supplier, verbose_name=trans("Default Supplier"), null=True, blank=True)
    defaultcurrency = models.ForeignKey(Currency, verbose_name=trans("Default Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=trans("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=trans("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=trans("Last modified by"), related_name="db_contractlstmodified")

    class Meta:
        app_label = "crm"
        verbose_name = trans('Contract')
        verbose_name_plural = trans('Contracts')

    def create_invoice(self):
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

    def create_quote(self):
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

    def create_purchase_order(self):
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

    def __unicode__(self):
        return trans("Contract") + " " + str(self.id)


class PurchaseOrder(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=trans("Contract"))
    externalReference = models.CharField(verbose_name=trans("External Reference"), max_length=100, blank=True,
                                         null=True)
    supplier = models.ForeignKey(Supplier, verbose_name=trans("Supplier"))
    description = models.CharField(verbose_name=trans("Description"), max_length=100, blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=trans("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2,
                                              verbose_name=trans("Last Calculted Price With Tax"), blank=True,
                                              null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=trans("Last Calculted Tax"),
                                            blank=True, null=True)
    status = models.CharField(max_length=1, choices=PURCHASEORDERSTATUS)
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=trans("Staff"),
                              related_name="db_relpostaff", null=True)
    currency = models.ForeignKey(Currency, verbose_name=trans("Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=trans("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=trans("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=trans("Last modified by"), related_name="db_polstmodified")

    def recalculate_prices(self, pricing_date):
        price = 0
        tax = 0
        try:
            positions = PurchaseOrderPosition.objects.filter(contract=self.id)
            if type(positions) == PurchaseOrderPosition:
                if type(self.discount) == Decimal:
                    price = int(positions.recalculate_prices(pricing_date, self.customer, self.currency) * (
                        1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    tax = int(positions.recalculate_tax(self.currency) * (
                        1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                else:
                    price = positions.recalculate_prices(pricing_date, self.customer, self.currency)
                    tax = positions.recalculate_tax(self.currency)
            else:
                for position in positions:
                    if type(self.discount) == Decimal:
                        price += int(position.recalculate_prices(pricing_date, self.customer, self.currency) * (
                            1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                        tax += int(position.recalculate_tax(self.currency) * (
                            1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    else:
                        price += position.recalculate_prices(pricing_date, self.customer, self.currency)
                        tax += position.recalculate_tax(self.currency)
            self.lastCalculatedPrice = price
            self.lastCalculatedTax = tax
            self.lastPricingDate = pricing_date
            self.save()
            return 1
        except Quote.DoesNotExist, e:
            print "ERROR " + e.__str__()
            print "Der Fehler trat beim File: " + self.sourcefile
            exit()
            return 0

    def create_pdf(self, what_to_export):
        xml_serializer = serializers.get_serializer("xml")
        xml_serializer = xml_serializer()
        out = open(settings.PDF_OUTPUT_ROOT + "purchaseorder_" + str(self.id) + ".xml", "w")
        objects_to_serialize = list(PurchaseOrder.objects.filter(id=self.id))
        objects_to_serialize += list(Contact.objects.filter(id=self.supplier.id))
        objects_to_serialize += list(Currency.objects.filter(id=self.currency.id))
        objects_to_serialize += list(PurchaseOrderPosition.objects.filter(contract=self.id))
        for position in list(PurchaseOrderPosition.objects.filter(contract=self.id)):
            objects_to_serialize += list(Position.objects.filter(id=position.id))
            objects_to_serialize += list(Product.objects.filter(id=position.product.id))
            objects_to_serialize += list(Unit.objects.filter(id=position.unit.id))
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.staff.id))
        user_extension = djangoUserExtension.models.UserExtension.objects.filter(user=self.staff.id)
        if len(user_extension) == 0:
            raise Exception(trans("During PurchaseOrder PDF Export"))
        phone_address = djangoUserExtension.models.UserExtensionPhoneAddress.objects.filter(
            userExtension=user_extension[0].id)
        objects_to_serialize += list(user_extension)
        objects_to_serialize += list(phone_address)
        templateset = djangoUserExtension.models.TemplateSet.objects.filter(id=user_extension[0].defaultTemplateSet.id)
        if len(templateset) == 0:
            raise Exception(trans("During PurchaseOrder PDF Export"))
        objects_to_serialize += list(templateset)
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objects_to_serialize += list(PostalAddressForContact.objects.filter(person=self.supplier.id))
        for address in list(PostalAddressForContact.objects.filter(person=self.supplier.id)):
            objects_to_serialize += list(PostalAddress.objects.filter(id=address.id))
        xml_serializer.serialize(objects_to_serialize, stream=out, indent=3)
        out.close()
        check_output(['/usr/bin/fop', '-c', user_extension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml',
                      settings.PDF_OUTPUT_ROOT + 'purchaseorder_' + str(self.id) + '.xml', '-xsl',
                      user_extension[0].defaultTemplateSet.purchaseorderXSLFile.xslfile.path, '-pdf',
                      settings.PDF_OUTPUT_ROOT + 'purchaseorder_' + str(self.id) + '.pdf'], stderr=STDOUT)
        return settings.PDF_OUTPUT_ROOT + "purchaseorder_" + str(self.id) + ".pdf"

    class Meta:
        app_label = "crm"
        verbose_name = trans('Purchase Order')
        verbose_name_plural = trans('Purchase Order')

    def __unicode__(self):
        return trans("Purchase Order") + ": " + str(self.id) + " " + trans("from Contract") + ": " + str(
            self.contract.id)


class SalesContract(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=trans('Contract'))
    externalReference = models.CharField(verbose_name=trans("External Reference"), max_length=100, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=trans("Discount"), blank=True,
                                   null=True)
    description = models.CharField(verbose_name=trans("Description"), max_length=100, blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=trans("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2,
                                              verbose_name=trans("Last Calculted Price With Tax"), blank=True,
                                              null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=trans("Last Calculted Tax"),
                                            blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name=trans("Customer"))
    staff = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True}, blank=True, verbose_name=trans("Staff"),
                              related_name="db_relscstaff", null=True)
    currency = models.ForeignKey(Currency, verbose_name=trans("Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=trans("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=trans("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=trans("Last modified by"), related_name="db_lstscmodified",
                                       null=True,
                                       blank="True")

    def recalculate_prices(self, pricing_date):
        price = 0
        tax = 0
        try:
            positions = SalesContractPosition.objects.filter(contract=self.id)
            if type(positions) == SalesContractPosition:
                if type(self.discount) == Decimal:
                    price = int(positions.recalculate_prices(pricing_date, self.customer, self.currency) * (
                        1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    tax = int(positions.recalculate_tax(self.currency) * (
                        1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                else:
                    price = positions.recalculate_prices(pricing_date, self.customer, self.currency)
                    tax = positions.recalculate_tax(self.currency)
            else:
                for position in positions:
                    price += position.recalculate_prices(pricing_date, self.customer, self.currency)
                    tax += position.recalculate_tax(self.currency)
                if type(self.discount) == Decimal:
                    price = int(price * (1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding
                    tax = int(tax * (1 - self.discount / 100) / self.currency.rounding) * self.currency.rounding

            self.lastCalculatedPrice = price
            self.lastCalculatedTax = tax
            self.lastPricingDate = pricing_date
            self.save()
            return 1
        except Quote.DoesNotExist:
            return 0

    class Meta:
        app_label = "crm"
        verbose_name = trans('Sales Contract')
        verbose_name_plural = trans('Sales Contracts')

    def __unicode__(self):
        return trans("Sales Contract") + ": " + str(self.id) + " " + trans("from Contract") + ": " + str(
            self.contract.id)


class Quote(SalesContract):
    validuntil = models.DateField(verbose_name=trans("Valid until"))
    status = models.CharField(max_length=1, choices=QUOTESTATUS, verbose_name=trans('Status'))

    def create_invoice(self):
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
            quote_positions = SalesContractPosition.objects.filter(contract=self.id)
            for quotePosition in list(quote_positions):
                invoice_position = SalesContractPosition()
                invoice_position.product = quotePosition.product
                invoice_position.positionNumber = quotePosition.positionNumber
                invoice_position.quantity = quotePosition.quantity
                invoice_position.description = quotePosition.description
                invoice_position.discount = quotePosition.discount
                invoice_position.product = quotePosition.product
                invoice_position.unit = quotePosition.unit
                invoice_position.sentOn = quotePosition.sentOn
                invoice_position.supplier = quotePosition.supplier
                invoice_position.shipmentID = quotePosition.shipmentID
                invoice_position.overwriteProductPrice = quotePosition.overwriteProductPrice
                invoice_position.positionPricePerUnit = quotePosition.positionPricePerUnit
                invoice_position.lastPricingDate = quotePosition.lastPricingDate
                invoice_position.lastCalculatedPrice = quotePosition.lastCalculatedPrice
                invoice_position.lastCalculatedTax = quotePosition.lastCalculatedTax
                invoice_position.contract = invoice
                invoice_position.save()
            return invoice
        except Quote.DoesNotExist:
            return

    def create_pdf(self, what_to_export):
        xml_serializer = serializers.get_serializer("xml")
        xml_serializer = xml_serializer()
        out = open(settings.PDF_OUTPUT_ROOT + "quote_" + str(self.id) + ".xml", "w")
        objects_to_serialize = list(Quote.objects.filter(id=self.id))
        objects_to_serialize += list(SalesContract.objects.filter(id=self.id))
        objects_to_serialize += list(Contact.objects.filter(id=self.customer.id))
        objects_to_serialize += list(Currency.objects.filter(id=self.currency.id))
        objects_to_serialize += list(SalesContractPosition.objects.filter(contract=self.id))
        for position in list(SalesContractPosition.objects.filter(contract=self.id)):
            objects_to_serialize += list(Position.objects.filter(id=position.id))
            objects_to_serialize += list(Product.objects.filter(id=position.product.id))
            objects_to_serialize += list(Unit.objects.filter(id=position.unit.id))
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.staff.id))
        user_extension = djangoUserExtension.models.UserExtension.objects.filter(user=self.staff.id)
        if len(user_extension) == 0:
            raise Exception(trans("During Quote PDF Export"))
        phone_address = djangoUserExtension.models.UserExtensionPhoneAddress.objects.filter(
            userExtension=user_extension[0].id)
        objects_to_serialize += list(user_extension)
        objects_to_serialize += list(PhoneAddress.objects.filter(id=phone_address[0].id))
        templateset = djangoUserExtension.models.TemplateSet.objects.filter(id=user_extension[0].defaultTemplateSet.id)
        if len(templateset) == 0:
            raise Exception(trans("During Quote PDF Export"))
        objects_to_serialize += list(templateset)
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objects_to_serialize += list(PostalAddressForContact.objects.filter(person=self.customer.id))
        for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
            objects_to_serialize += list(PostalAddress.objects.filter(id=address.id))
        xml_serializer.serialize(objects_to_serialize, stream=out, indent=3)
        out.close()
        xml = etree.parse(settings.PDF_OUTPUT_ROOT + "quote_" + str(self.id) + ".xml")
        rootelement = xml.getroot()
        projectroot = etree.SubElement(rootelement, "projectroot")
        projectroot.text = settings.PROJECT_ROOT
        xml.write(settings.PDF_OUTPUT_ROOT + "quote_" + str(self.id) + ".xml")
        if what_to_export == "quote":
            check_output(['/usr/bin/fop', '-c', user_extension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml',
                          settings.PDF_OUTPUT_ROOT + 'quote_' + str(self.id) + '.xml', '-xsl',
                          user_extension[0].defaultTemplateSet.quoteXSLFile.xslfile.path, '-pdf',
                          settings.PDF_OUTPUT_ROOT + 'quote_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "quote_" + str(self.id) + ".pdf"
        else:
            check_output(['/usr/bin/fop', '-c', user_extension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml',
                          settings.PDF_OUTPUT_ROOT + 'quote_' + str(self.id) + '.xml', '-xsl',
                          user_extension[0].defaultTemplateSet.purchaseconfirmationXSLFile.xslfile.path, '-pdf',
                          settings.PDF_OUTPUT_ROOT + 'purchaseconfirmation_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "purchaseconfirmation_" + str(self.id) + ".pdf"

    def __unicode__(self):
        return trans("Quote") + ": " + str(self.id) + " " + trans("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Quote')
        verbose_name_plural = trans('Quotes')


class Invoice(SalesContract):
    payableuntil = models.DateField(verbose_name=trans("To pay until"))
    derivatedFromQuote = models.ForeignKey(Quote, blank=True, null=True)
    paymentBankReference = models.CharField(verbose_name=trans("Payment Bank Reference"), max_length=100, blank=True,
                                            null=True)
    status = models.CharField(max_length=1, choices=INVOICESTATUS)

    def register_invoice_in_accounting(self, request):
        dictprices = dict()
        dicttax = dict()
        exists = False
        current_valid_accounting_period = accounting.models.AccountingPeriod.get_current_valid_accounting_period()
        activaaccount = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        for position in list(SalesContractPosition.objects.filter(contract=self.id)):
            profitaccount = position.product.accoutingProductCategorie.profitAccount
            dictprices[profitaccount] = position.lastCalculatedPrice
            dicttax[profitaccount] = position.lastCalculatedTax

        for booking in accounting.models.Booking.objects.filter(accountingPeriod=current_valid_accounting_period):
            if booking.bookingReference == self:
                raise Exception("Invoice already registered")
            for profitaccount, amount in dictprices.iteritems():
                booking = accounting.models.Booking()
                booking.toAccount = activaaccount[0]
                booking.fromAccount = profitaccount
                booking.bookingReference = self
                booking.accountingPeriod = current_valid_accounting_period
                booking.bookingDate = date.today().__str__()
                booking.staff = request.user
                booking.amount = amount
                booking.lastmodifiedby = request.user
                booking.save()

    def register_payment_in_accounting(self, request, paymentaccount, amount, payment_date):
        activaaccount = accounting.Account.objects.filter(isopeninterestaccount=True)
        booking = accounting.Booking()
        booking.toAccount = activaaccount
        booking.fromAccount = paymentaccount
        booking.bookingDate = payment_date.today().__str__()
        booking.bookingReference = self
        booking.accountingPeriod = accounting.models.AccountingPeriod.objects.all()[0]
        booking.amount = self.lastCalculatedPrice
        booking.staff = request.user
        booking.lastmodifiedby = request.user
        booking.save()

    def create_pdf(self, what_to_export):
        xml_serializer = serializers.get_serializer("xml")
        xml_serializer = xml_serializer()
        out = open(settings.PDF_OUTPUT_ROOT + "invoice_" + str(self.id) + ".xml", "w")
        objects_to_serialize= list(Invoice.objects.filter(id=self.id))
        objects_to_serialize += list(SalesContract.objects.filter(id=self.id))
        objects_to_serialize += list(Contact.objects.filter(id=self.customer.id))
        objects_to_serialize += list(Currency.objects.filter(id=self.currency.id))
        objects_to_serialize += list(SalesContractPosition.objects.filter(contract=self.id))
        for position in list(SalesContractPosition.objects.filter(contract=self.id)):
            objects_to_serialize += list(Position.objects.filter(id=position.id))
            objects_to_serialize += list(Product.objects.filter(id=position.product.id))
            objects_to_serialize += list(Unit.objects.filter(id=position.unit.id))
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.staff.id))
        user_extension = djangoUserExtension.models.UserExtension.objects.filter(user=self.staff.id)
        if len(user_extension) == 0:
            raise Exception(trans("During Invoice PDF Export"))
        phone_address = djangoUserExtension.models.UserExtensionPhoneAddress.objects.filter(
            userExtension=user_extension[0].id)
        objects_to_serialize += list(user_extension)
        objects_to_serialize += list(PhoneAddress.objects.filter(id=phone_address[0].id))
        templateset = djangoUserExtension.models.TemplateSet.objects.filter(id=user_extension[0].defaultTemplateSet.id)
        if len(templateset) == 0:
            raise Exception(trans("During Invoice PDF Export"))
        objects_to_serialize += list(templateset)
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objects_to_serialize += list(PostalAddressForContact.objects.filter(person=self.customer.id))
        for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
            objects_to_serialize += list(PostalAddress.objects.filter(id=address.id))
        xml_serializer.serialize(objects_to_serialize, stream=out, indent=3)
        out.close()
        xml = etree.parse(settings.PDF_OUTPUT_ROOT + "invoice_" + str(self.id) + ".xml")
        rootelement = xml.getroot()
        projectroot = etree.SubElement(rootelement, "projectroot")
        projectroot.text = settings.PROJECT_ROOT
        xml.write(settings.PDF_OUTPUT_ROOT + "invoice_" + str(self.id) + ".xml")
        if what_to_export == "invoice":
            check_output(['/usr/bin/fop', '-c', user_extension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml',
                          settings.PDF_OUTPUT_ROOT + 'invoice_' + str(self.id) + '.xml', '-xsl',
                          user_extension[0].defaultTemplateSet.invoiceXSLFile.xslfile.path, '-pdf',
                          settings.PDF_OUTPUT_ROOT + 'invoice_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "invoice_" + str(self.id) + ".pdf"
        else:
            check_output(['/usr/bin/fop', '-c', user_extension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml',
                          settings.PDF_OUTPUT_ROOT + 'invoice_' + str(self.id) + '.xml', '-xsl',
                          user_extension[0].defaultTemplateSet.deilveryorderXSLFile.xslfile.path, '-pdf',
                          settings.PDF_OUTPUT_ROOT + 'deliveryorder_' + str(self.id) + '.pdf'], stderr=STDOUT)
            return settings.PDF_OUTPUT_ROOT + "deliveryorder_" + str(self.id) + ".pdf"

            # TODO: def registerPayment(self, amount, register_payment_in_accounting):

    def __unicode__(self):
        return trans("Invoice") + ": " + str(self.id) + " " + trans("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Invoice')
        verbose_name_plural = trans('Invoices')


class Unit(models.Model):
    description = models.CharField(verbose_name=trans("Description"), max_length=100)
    shortName = models.CharField(verbose_name=trans("Displayed Name After Quantity In The Position"), max_length=3)
    isAFractionOf = models.ForeignKey('self', blank=True, null=True, verbose_name=trans("Is A Fraction Of"))
    fractionFactorToNextHigherUnit = models.IntegerField(verbose_name=trans("Factor Between This And Next Higher Unit"),
                                                         blank=True, null=True)

    def __unicode__(self):
        return self.shortName

    class Meta:
        app_label = "crm"
        verbose_name = trans('Unit')
        verbose_name_plural = trans('Units')


class Tax(models.Model):
    taxrate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=trans("Taxrate in Percentage"))
    name = models.CharField(verbose_name=trans("Taxname"), max_length=100)
    accountActiva = models.ForeignKey('accounting.Account', verbose_name=trans("Activa Account"),
                                      related_name="db_relaccountactiva", null=True, blank=True)
    accountPassiva = models.ForeignKey('accounting.Account', verbose_name=trans("Passiva Account"),
                                       related_name="db_relaccountpassiva", null=True, blank=True)

    def getTaxRate(self):
        return self.taxrate

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "crm"
        verbose_name = trans('Tax')
        verbose_name_plural = trans('Taxes')


class Product(models.Model):
    description = models.TextField(verbose_name=trans("Description"), null=True, blank=True)
    title = models.CharField(verbose_name=trans("Title"), max_length=200)
    productNumber = models.IntegerField(verbose_name=trans("Product Number"))
    defaultunit = models.ForeignKey(Unit, verbose_name=trans("Unit"))
    dateofcreation = models.DateTimeField(verbose_name=trans("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=trans("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=trans("Last modified by"), null=True, blank="True")
    tax = models.ForeignKey(Tax, blank=False)
    accoutingProductCategorie = models.ForeignKey('accounting.ProductCategory',
                                                  verbose_name=trans("Accounting Product Categorie"), null=True,
                                                  blank="True")

    def get_price(self, date, unit, customer, currency):
        prices = Price.objects.filter(product=self.id)
        unit_transforms = UnitTransform.objects.filter(product=self.id)
        customer_group_transforms = CustomerGroupTransform.objects.filter(product=self.id)
        validpriceslist = list()
        for price in list(prices):
            for customerGroup in CustomerGroup.objects.filter(customer=customer):
                if price.matches_date_unit_customer_group_currency(date, unit, customerGroup, currency):
                    validpriceslist.append(price.price)
                else:
                    for customerGroupTransform in customer_group_transforms:
                        if price.matches_date_unit_customer_group_currency(date, unit,
                                                                      customerGroupTransform.transform(customerGroup),
                                                                      currency):
                            validpriceslist.append(price.price * customerGroup.factor)
                        else:
                            for unitTransfrom in list(unit_transforms):
                                if price.matches_date_unit_customer_group_currency(date,
                                                                              unitTransfrom.transfrom(unit).transform(
                                                                                      unitTransfrom),
                                                                              customerGroupTransform.transform(
                                                                                      customerGroup), currency):
                                    validpriceslist.append(
                                        price.price * customerGroupTransform.factor * unitTransfrom.factor)
        if len(validpriceslist) > 0:
            lowestprice = validpriceslist[0]
            for price in validpriceslist:
                if price < lowestprice:
                    lowestprice = price
            return lowestprice
        else:
            raise Product.NoPriceFound(customer, unit, date, self)

    def get_tax_rate(self):
        return self.tax.getTaxRate()

    def __unicode__(self):
        return str(self.productNumber) + ' ' + self.title

    class Meta:
        app_label = "crm"
        verbose_name = trans('Product')
        verbose_name_plural = trans('Products')

    class NoPriceFound(Exception):
        def __init__(self, customer, unit, date, product):
            self.customer = customer
            self.unit = unit
            self.date = date
            self.product = product
            return

        def __str__(self):
            return trans("There is no Price for this product") + ": " + self.product.__unicode__() + trans(
                "that matches the date") + ": " + self.date.__str__() + " ," + trans(
                "customer") + ": " + self.customer.__unicode__() + trans(" and unit") + ":" + self.unit.__unicode__()


class UnitTransform(models.Model):
    fromUnit = models.ForeignKey('Unit', verbose_name=trans("From Unit"), related_name="db_reltransfromfromunit")
    toUnit = models.ForeignKey('Unit', verbose_name=trans("To Unit"), related_name="db_reltransfromtounit")
    product = models.ForeignKey('Product', verbose_name=trans("Product"))
    factor = models.IntegerField(verbose_name=trans("Factor between From and To Unit"), blank=True, null=True)

    def transform(self, unit):
        if self.fromUnit == unit:
            return self.toUnit
        else:
            return unit

    def __unicode__(self):
        return "From " + self.fromUnit.shortName + " to " + self.toUnit.shortName

    class Meta:
        app_label = "crm"
        verbose_name = trans('Unit Transfrom')
        verbose_name_plural = trans('Unit Transfroms')


class CustomerGroupTransform(models.Model):
    fromCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name=trans("From Unit"),
                                          related_name="db_reltransfromfromcustomergroup")
    toCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name=trans("To Unit"),
                                        related_name="db_reltransfromtocustomergroup")
    product = models.ForeignKey('Product', verbose_name=trans("Product"))
    factor = models.IntegerField(verbose_name=trans("Factor between From and To Customer Group"), blank=True, null=True)

    def transform(self, customer_group):
        if self.fromCustomerGroup == customer_group:
            return self.toCustomerGroup
        else:
            return customer_group

    def __unicode__(self):
        return "From " + self.fromCustomerGroup.name + " to " + self.toCustomerGroup.name

    class Meta:
        app_label = "crm"
        verbose_name = trans('Customer Group Price Transfrom')
        verbose_name_plural = trans('Customer Group Price Transfroms')


class Price(models.Model):
    product = models.ForeignKey(Product, verbose_name=trans("Product"))
    unit = models.ForeignKey(Unit, blank=False, verbose_name=trans("Unit"))
    currency = models.ForeignKey(Currency, blank=False, null=False, verbose_name='Currency')
    customerGroup = models.ForeignKey(CustomerGroup, blank=True, null=True, verbose_name=trans("Customer Group"))
    price = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=trans("Price Per Unit"))
    validfrom = models.DateField(verbose_name=trans("Valid from"), blank=True, null=True)
    validuntil = models.DateField(verbose_name=trans("Valid until"), blank=True, null=True)

    def matches_date_unit_customer_group_currency(self, date, unit, customer_group, currency):
        if self.validfrom == None:
            if self.validuntil == None:
                if self.customerGroup == None:
                    if (unit == self.unit) & (self.currency == currency):
                        return 1
                else:
                    if (unit == self.unit) & (self.customerGroup == customer_group) & (self.currency == currency):
                        return 1
            elif self.customerGroup == None:
                if ((date - self.validuntil).days < 0) & (unit == self.unit) & (self.currency == currency):
                    return 1
            else:
                if ((date - self.validuntil).days < 0) & (unit == self.unit) & (self.customerGroup == customer_group) & (
                            self.currency == currency):
                    return 1
        elif self.validuntil == None:
            if self.customerGroup == None:
                if ((self.validfrom - date).days < 0) & (unit == self.unit) & (self.currency == currency):
                    return 1
            else:
                if ((self.validfrom - date).days < 0) & (unit == self.unit) & (self.customerGroup == customer_group) & (
                            self.currency == currency):
                    return 1
        elif self.customerGroup == None:
            if ((self.validfrom - date).days < 0) & (self.validuntil == None) & (unit == self.unit) & (
                        self.customerGroup == None) & (self.currency == currency):
                return 1
        else:
            if ((self.validfrom - date).days < 0) & ((date - self.validuntil).days < 0) & (unit == self.unit) & (
                        self.customerGroup == customer_group) & (self.currency == currency):
                return 1

    class Meta:
        app_label = "crm"
        verbose_name = trans('Price')
        verbose_name_plural = trans('Prices')


class Position(models.Model):
    positionNumber = models.IntegerField(verbose_name=trans("Position Number"))
    quantity = models.DecimalField(verbose_name=trans("Quantity"), decimal_places=3, max_digits=10)
    description = models.TextField(verbose_name=trans("Description"), blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=trans("Discount"), blank=True,
                                   null=True)
    product = models.ForeignKey(Product, verbose_name=trans("Product"), blank=True, null=True)
    unit = models.ForeignKey(Unit, verbose_name=trans("Unit"), blank=True, null=True)
    sentOn = models.DateField(verbose_name=trans("Shipment on"), blank=True, null=True)
    supplier = models.ForeignKey(Supplier, verbose_name=trans("Shipment Supplier"),
                                 limit_choices_to={'offersShipmentToCustomers': True}, blank=True, null=True)
    shipmentID = models.CharField(max_length=100, verbose_name=trans("Shipment ID"), blank=True, null=True)
    overwriteProductPrice = models.BooleanField(verbose_name=trans('Overwrite Product Price'), default=False)
    positionPricePerUnit = models.DecimalField(verbose_name=trans("Price Per Unit"), max_digits=17, decimal_places=2,
                                               blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=trans("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2,
                                              verbose_name=trans("Last Calculted Price"),
                                              blank=True, null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=trans("Last Calculted Tax"),
                                            blank=True, null=True)

    def recalculate_prices(self, pricing_date, customer, currency):
        if not self.overwriteProductPrice:
            self.positionPricePerUnit = self.product.get_price(pricing_date, self.unit, customer, currency)
        if type(self.discount) == Decimal:
            self.lastCalculatedPrice = int(self.positionPricePerUnit * self.quantity * (
                1 - self.discount / 100) / currency.rounding) * currency.rounding
        else:
            self.lastCalculatedPrice = self.positionPricePerUnit * self.quantity
        self.lastPricingDate = pricing_date
        self.save()
        return self.lastCalculatedPrice

    def recalculate_tax(self, currency):
        if type(self.discount) == Decimal:
            self.lastCalculatedTax = int(self.product.get_tax_rate() / 100 * self.positionPricePerUnit * self.quantity * (
                1 - self.discount / 100) / currency.rounding) * currency.rounding
        else:
            self.lastCalculatedTax = self.product.get_tax_rate() / 100 * self.positionPricePerUnit * self.quantity
        self.save()
        return self.lastCalculatedTax

    def __unicode__(self):
        return trans("Position") + ": " + str(self.id)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Position')
        verbose_name_plural = trans('Positions')


class SalesContractPosition(Position):
    contract = models.ForeignKey(SalesContract, verbose_name=trans("Contract"))

    class Meta:
        app_label = "crm"
        verbose_name = trans('Salescontract Position')
        verbose_name_plural = trans('Salescontract Positions')

    def __unicode__(self):
        return trans("Salescontract Position") + ": " + str(self.id)


class PurchaseOrderPosition(Position):
    contract = models.ForeignKey(PurchaseOrder, verbose_name=trans("Contract"))

    class Meta:
        app_label = "crm"
        verbose_name = trans('Purchaseorder Position')
        verbose_name_plural = trans('Purchaseorder Positions')

    def __unicode__(self):
        return trans("Purchaseorder Position") + ": " + str(self.id)


class PhoneAddressForContact(PhoneAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Phone Address For Contact')
        verbose_name_plural = trans('Phone Address For Contact')

    def __unicode__(self):
        return str(self.phone)


class EmailAddressForContact(EmailAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Email Address For Contact')
        verbose_name_plural = trans('Email Address For Contact')

    def __unicode__(self):
        return str(self.email)


class PostalAddressForContact(PostalAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER)
    person = models.ForeignKey(Contact)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Postal Address For Contact')
        verbose_name_plural = trans('Postal Address For Contact')

    def __unicode__(self):
        return self.prename + ' ' + self.name + ' ' + self.addressline1


class PostalAddressForContract(PostalAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(Contract)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Postal Address For Contracts')
        verbose_name_plural = trans('Postal Address For Contracts')

    def __unicode__(self):
        return self.prename + ' ' + self.name + ' ' + self.addressline1


class PostalAddressForPurchaseOrder(PostalAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(PurchaseOrder)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Postal Address For Contracts')
        verbose_name_plural = trans('Postal Address For Contracts')

    def __unicode__(self):
        return self.prename + ' ' + self.name + ' ' + self.addressline1


class PostalAddressForSalesContract(PostalAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(SalesContract)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Postal Address For Contracts')
        verbose_name_plural = trans('Postal Address For Contracts')

    def __unicode__(self):
        return self.prename + ' ' + self.name + ' ' + self.addressline1


class PhoneAddressForContract(PhoneAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(Contract)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Phone Address For Contracts')
        verbose_name_plural = trans('Phone Address For Contracts')

    def __unicode__(self):
        return str(self.phone)


class PhoneAddressForSalesContract(PhoneAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(SalesContract)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Phone Address For Contracts')
        verbose_name_plural = trans('Phone Address For Contracts')

    def __unicode__(self):
        return str(self.phone)


class PhoneAddressForPurchaseOrder(PhoneAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(PurchaseOrder)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Phone Address For Contracts')
        verbose_name_plural = trans('Phone Address For Contracts')

    def __unicode__(self):
        return str(self.phone)


class EmailAddressForContract(EmailAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(Contract)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Email Address For Contracts')
        verbose_name_plural = trans('Email Address For Contracts')

    def __unicode__(self):
        return str(self.email)


class EmailAddressForSalesContract(EmailAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(SalesContract)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Email Address For Contracts')
        verbose_name_plural = trans('Email Address For Contracts')

    def __unicode__(self):
        return str(self.email)


class EmailAddressForPurchaseOrder(EmailAddress):
    purpose = models.CharField(verbose_name=trans("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    contract = models.ForeignKey(PurchaseOrder)

    class Meta:
        app_label = "crm"
        verbose_name = trans('Email Address For Contracts')
        verbose_name_plural = trans('Email Address For Contracts')

    def __unicode__(self):
        return str(self.email)
    
