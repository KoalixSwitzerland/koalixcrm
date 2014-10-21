# -*- coding: utf-8 -*-

from datetime import date, timedelta
from decimal import Decimal
from subprocess import check_output, STDOUT
from xml import etree
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
from django.contrib import auth
from filebrowser_safe.fields import FileBrowseField
from django_fsm import FSMIntegerField, transition
from mezzanine.core.models import Displayable

from const.country import COUNTRIES
from const.postaladdressprefix import POSTALADDRESSPREFIX
from const.purpose import PURPOSESADDRESSINCONTRACT, PURPOSESADDRESSINCUSTOMER
from const.states import InvoiceStatesEnum, PurchaseOrderStatesEnum, QuoteStatesEnum
# from accounting.models import Booking, Account, AccountingPeriod


# ###########################
# ##   Contact Additions   ##
# ###########################


class PostalAddress(models.Model):
    addressline1 = models.CharField(max_length=200, verbose_name=_("Addressline 1"), blank=True, null=True)
    addressline2 = models.CharField(max_length=200, verbose_name=_("Addressline 2"), blank=True, null=True)
    # tfr, 10-13-14, v0.2: I'm not sure if these are really needed. Leaving outcommented for a few releases
    # addressline3 = models.CharField(max_length=200, verbose_name=_("Addressline 3"), blank=True, null=True)
    # addressline4 = models.CharField(max_length=200, verbose_name=_("Addressline 4"), blank=True, null=True)
    zipcode = models.IntegerField(verbose_name=_("Zipcode"), blank=True, null=True)
    town = models.CharField(max_length=100, verbose_name=_("City"), blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name=_("State"), blank=True, null=True)
    country = models.CharField(max_length=2, choices=[(x[0], x[3]) for x in COUNTRIES], verbose_name=_("Country"),
                               blank=True, null=True)
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT, default='C')
    person = models.ForeignKey('Contact', related_name='addresses')

    class Meta():
        verbose_name = _('Postal Address')
        verbose_name_plural = _('Postal Address')
        permissions = (
            ('view_postaladdress', 'Can view postal address'),
        )

    def __unicode__(self):
        return '%s, %d %s' % (self.addressline1, self.zipcode, self.town)


class PhoneAddress(models.Model):
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCUSTOMER, default='H')
    person = models.ForeignKey('Contact', related_name='phonenumbers')

    class Meta():
        verbose_name = _('Phone Address')
        verbose_name_plural = _('Phone Address')
        permissions = (
            ('view_phoneaddress', 'Can view phone address'),
        )

    def __unicode__(self):
        return "%s: %s" % (self.purpose, self.phone)


class EmailAddress(models.Model):
    email = models.EmailField(max_length=200, verbose_name=_("Email Address"))
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT, default='C')
    person = models.ForeignKey('Contact', related_name='emailaddresses')

    class Meta():
        verbose_name = _('Email Address')
        verbose_name_plural = _('Email Address')
        permissions = (
            ('view_emailaddress', 'Can view email address'),
        )

    def __unicode__(self):
        return "%s: %s" % (self.purpose, self.email)


# ########################
# ##    PARTICIPANTS    ##
# ########################


class Contact(models.Model):
    prefix = models.CharField(max_length=1, choices=POSTALADDRESSPREFIX, verbose_name=_("Prefix"), blank=True,
                              null=True)
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True,
                                       verbose_name=_("Last modified by"), null=True)

    class Meta():
        verbose_name = _('Contact')
        verbose_name_plural = _('Contact')
        permissions = (
            ('view_contact', 'Can view contact'),
        )

    def __unicode__(self):
        return self.name


class CustomerGroup(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

    class Meta():
        verbose_name = _('Customer Group')
        verbose_name_plural = _('Customer Groups')
        permissions = (
            ('view_customer_group', 'Can view customer groups'),
        )


class Customer(Displayable, Contact):
    firstname = models.CharField(max_length=300, verbose_name=_("Prename"), blank=True)
    billingcycle = models.ForeignKey('CustomerBillingCycle', verbose_name=_('Default Billing Cycle'))
    ismemberof = models.ManyToManyField(CustomerGroup, verbose_name=_('Is member of'), blank=True, null=True)
    search_fields = {"name": 10, "firstname": 8}

    class Meta():
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        permissions = (
            ('view_customer', 'Can view customers'),
        )

    def get_absolute_url(self):
        url = '/customers/detail/' + str(self.pk)  # TODO: Bad solution
        return url

    def create_contract(self, request):
        contract = Contract()
        contract.defaultcustomer = self
        contract.defaultcurrency = UserExtension.objects.filter(user=request.user.id)[0].defaultCurrency
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

    def __unicode__(self):
        return "%s %s %s" % (self.prefix, self.firstname, self.name)


class Supplier(Displayable, Contact):
    direct_shipment_to_customers = models.BooleanField(verbose_name=_("Offers direct Shipment to Customer"),
                                                       default=False)
    search_fields = {"name": 10}

    class Meta():
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")
        permissions = (
            ('view_supplier', 'Can view suppliers'),
        )

    def get_absolute_url(self):
        url = '/suppliers/detail/' + str(self.pk)  # TODO: Bad solution
        return url

    def __unicode__(self):
        return self.name


# ###########################
# ##    PAYMENT RELATED    ##
# ###########################


class CustomerBillingCycle(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    days_to_payment = models.IntegerField(verbose_name=_("Days To Payment Date"))

    class Meta():
        verbose_name = _('Customer Billing Cycle')
        verbose_name_plural = _('Customer Billing Cycle')
        permissions = (
            ('view_customerbillingcycle', 'Can view billing cycles'),
        )

    def __unicode__(self):
        return self.name


class Currency(models.Model):
    description = models.CharField(verbose_name=_("Description"), max_length=100)
    shortname = models.CharField(verbose_name=_("Displayed Name After Price In The Position"), max_length=3)
    rounding = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Rounding"), blank=True, null=True)

    class Meta():
        verbose_name = _('Currency')
        verbose_name_plural = _('Currency')
        permissions = (
            ('view_currency', 'Can view currencies'),
        )

    def __unicode__(self):
        return self.shortname

# ##########################
# ##   CONTRACT RELATED   ##
# ##########################


class Contract(models.Model):
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relcontractstaff", null=True)
    description = models.TextField(verbose_name=_("Description"))
    defaultcustomer = models.ForeignKey(Customer, verbose_name=_("Default Customer"), null=True, blank=True)
    defaultSupplier = models.ForeignKey(Supplier, verbose_name=_("Default Supplier"), null=True, blank=True)
    defaultcurrency = models.ForeignKey(Currency, verbose_name=_("Default Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_contractlstmodified", null=True)

    class Meta():
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')
        permissions = (
            ('view_contract', 'Can view contracts'),
        )

    def create_invoice(self):
        invoice = Invoice()
        invoice.contract = self
        invoice.discount = 0
        invoice.staff = self.staff
        invoice.customer = self.defaultcustomer
        invoice.status = 'C'
        invoice.currency = self.defaultcurrency
        invoice.payableuntil = date.today() + timedelta(days=self.defaultcustomer.billingcycle.days_to_payment)
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
        return _("Contract") + " " + str(self.id)


class PurchaseOrder(models.Model):
    state = FSMIntegerField(default=PurchaseOrderStatesEnum.New)
    contract = models.ForeignKey(Contract, verbose_name=_("Contract"))
    externalReference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, verbose_name=_("Supplier"), blank=True, null=True)
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2,
                                              verbose_name=_("Last Calculted Price With Tax"), blank=True, null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"),
                                            blank=True, null=True)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relpostaff", null=True)
    currency = models.ForeignKey(Currency, verbose_name=_("Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_polstmodified", null=True, blank=True)

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

    @transition(field=state, source=PurchaseOrderStatesEnum.New, target=PurchaseOrderStatesEnum.Delayed)
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
        user_extension = UserExtension.objects.filter(user=self.staff.id)
        if len(user_extension) == 0:
            raise Exception(_("During PurchaseOrder PDF Export"))
        phone_address = PhoneAddress.objects.filter(
            userExtension=user_extension[0].id)
        objects_to_serialize += list(user_extension)
        objects_to_serialize += list(phone_address)
        templateset = TemplateSet.objects.filter(id=user_extension[0].defaultTemplateSet.id)
        if len(templateset) == 0:
            raise Exception(_("During PurchaseOrder PDF Export"))
        objects_to_serialize += list(templateset)
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objects_to_serialize += list(PostalAddress.objects.filter(person=self.supplier.id))
        for address in list(PostalAddress.objects.filter(person=self.supplier.id)):
            objects_to_serialize += list(PostalAddress.objects.filter(id=address.id))
        xml_serializer.serialize(objects_to_serialize, stream=out, indent=3)
        out.close()
        check_output(['/usr/bin/fop', '-c', user_extension[0].defaultTemplateSet.fopConfigurationFile.path, '-xml',
                      settings.PDF_OUTPUT_ROOT + 'purchaseorder_' + str(self.id) + '.xml', '-xsl',
                      user_extension[0].defaultTemplateSet.purchaseorderXSLFile.xslfile.path, '-pdf',
                      settings.PDF_OUTPUT_ROOT + 'purchaseorder_' + str(self.id) + '.pdf'], stderr=STDOUT)
        return settings.PDF_OUTPUT_ROOT + "purchaseorder_" + str(self.id) + ".pdf"

    class Meta():
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Order')
        permissions = (
            ('view_purchaseorder', 'Can view purchase orders'),
        )

    def __unicode__(self):
        return _("Purchase Order") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(
            self.contract.id)


class SalesContract(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=_('Contract'), related_name='contract')
    externalReference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True,
                                   null=True)
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2,
                                              verbose_name=_("Last Calculted Price With Tax"), blank=True,
                                              null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"),
                                            blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"))
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
                              related_name="db_relscstaff", null=True)
    currency = models.ForeignKey(Currency, verbose_name=_("Currency"), blank=False, null=False)
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_lstscmodified",
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

    class Meta():
        verbose_name = _('Sales Contract')
        verbose_name_plural = _('Sales Contracts')
        permissions = (
            ('view_salescontract', 'Can view sales contracts'),
        )

    def __unicode__(self):
        return _("Sales Contract") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(
            self.contract.id)


class Quote(SalesContract):
    state = FSMIntegerField(default=QuoteStatesEnum.New)
    validuntil = models.DateField(verbose_name=_("Valid until"))

    @transition(field=state, source=QuoteStatesEnum.New, target=QuoteStatesEnum.Quote_sent)
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
            days=self.customer.billingcycle.days_to_payment)
        invoice.dateofcreation = date.today().__str__()
        invoice.customerBillingCycle = self.customer.billingcycle
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

    @transition(field=state, source=QuoteStatesEnum.New, target=QuoteStatesEnum.Quote_created)
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
        user_extension = UserExtension.objects.filter(user=self.staff.id)
        if len(user_extension) == 0:
            raise Exception(_("During Quote PDF Export"))
        phone_address = PhoneAddress.objects.filter(
            userExtension=user_extension[0].id)
        objects_to_serialize += list(user_extension)
        objects_to_serialize += list(PhoneAddress.objects.filter(id=phone_address[0].id))
        templateset = TemplateSet.objects.filter(id=user_extension[0].defaultTemplateSet.id)
        if len(templateset) == 0:
            raise Exception(_("During Quote PDF Export"))
        objects_to_serialize += list(templateset)
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objects_to_serialize += list(PostalAddress.objects.filter(person=self.customer.id))
        for address in list(PostalAddress.objects.filter(person=self.customer.id)):
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

    class Meta():
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')
        permissions = (
            ('view_quote', 'Can view quotes'),
        )

    def __unicode__(self):
        return _("Quote") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)


class Invoice(SalesContract):
    state = FSMIntegerField(default=InvoiceStatesEnum.Open)
    payableuntil = models.DateField(verbose_name=_("To pay until"))
    derivatedFromQuote = models.ForeignKey(Quote, blank=True, null=True)
    paymentBankReference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                            null=True)

    # def register_invoice_in_accounting(self, request):
    #     dictprices = dict()
    #     dicttax = dict()
    #     exists = False
    #     current_valid_accounting_period = AccountingPeriod.get_current_valid_accounting_period()
    #     activaaccount = Account.objects.filter(isopeninterestaccount=True)
    #     for position in list(SalesContractPosition.objects.filter(contract=self.id)):
    #         profitaccount = position.product.accoutingProductCategorie.profitAccount
    #         dictprices[profitaccount] = position.lastCalculatedPrice
    #         dicttax[profitaccount] = position.lastCalculatedTax
    #
    #     for booking in Booking.objects.filter(accountingPeriod=current_valid_accounting_period):
    #         if booking.bookingReference == self:
    #             raise Exception("Invoice already registered")
    #         for profitaccount, amount in dictprices.iteritems():
    #             booking = Booking()
    #             booking.toAccount = activaaccount[0]
    #             booking.fromAccount = profitaccount
    #             booking.bookingReference = self
    #             booking.accountingPeriod = current_valid_accounting_period
    #             booking.bookingDate = date.today().__str__()
    #             booking.staff = request.user
    #             booking.amount = amount
    #             booking.lastmodifiedby = request.user
    #             booking.save()
    #
    # def register_payment_in_accounting(self, request, paymentaccount, amount, payment_date):
    #     activaaccount = Account.objects.filter(isopeninterestaccount=True)
    #     booking = Booking()
    #     booking.toAccount = activaaccount
    #     booking.fromAccount = paymentaccount
    #     booking.bookingDate = payment_date.today().__str__()
    #     booking.bookingReference = self
    #     booking.accountingPeriod = AccountingPeriod.objects.all()[0]
    #     booking.amount = self.lastCalculatedPrice
    #     booking.staff = request.user
    #     booking.lastmodifiedby = request.user
    #     booking.save()

    @transition(field=state, source=InvoiceStatesEnum.Open, target=InvoiceStatesEnum.Invoice_created)
    def create_pdf(self, what_to_export):
        xml_serializer = serializers.get_serializer("xml")
        xml_serializer = xml_serializer()
        out = open(settings.PDF_OUTPUT_ROOT + "invoice_" + str(self.id) + ".xml", "w")
        objects_to_serialize = list(Invoice.objects.filter(id=self.id))
        objects_to_serialize += list(SalesContract.objects.filter(id=self.id))
        objects_to_serialize += list(Contact.objects.filter(id=self.customer.id))
        objects_to_serialize += list(Currency.objects.filter(id=self.currency.id))
        objects_to_serialize += list(SalesContractPosition.objects.filter(contract=self.id))
        for position in list(SalesContractPosition.objects.filter(contract=self.id)):
            objects_to_serialize += list(Position.objects.filter(id=position.id))
            objects_to_serialize += list(Product.objects.filter(id=position.product.id))
            objects_to_serialize += list(Unit.objects.filter(id=position.unit.id))
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.staff.id))
        user_extension = UserExtension.objects.filter(user=self.staff.id)
        if len(user_extension) == 0:
            raise Exception(_("During Invoice PDF Export"))
        phone_address = PhoneAddress.objects.filter(
            userExtension=user_extension[0].id)
        objects_to_serialize += list(user_extension)
        objects_to_serialize += list(PhoneAddress.objects.filter(id=phone_address[0].id))
        templateset = TemplateSet.objects.filter(id=user_extension[0].defaultTemplateSet.id)
        if len(templateset) == 0:
            raise Exception(_("During Invoice PDF Export"))
        objects_to_serialize += list(templateset)
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objects_to_serialize += list(PostalAddress.objects.filter(person=self.customer.id))
        for address in list(PostalAddress.objects.filter(person=self.customer.id)):
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

    class Meta():
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        permissions = (
            ('view_invoice', 'Can view invoices'),
        )

    def __unicode__(self):
        return _("Invoice") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)


class Unit(models.Model):
    description = models.CharField(verbose_name=_("Description"), max_length=100)
    shortname = models.CharField(verbose_name=_("Displayed Name After Quantity In The Position"), max_length=3)
    fractionof = models.ForeignKey('self', blank=True, null=True, verbose_name=_("Is A Fraction Of"))
    factor = models.IntegerField(verbose_name=_("Factor Between This And Next Higher Unit"),
                                 blank=True, null=True)

    class Meta():
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        permissions = (
            ('view_unit', 'Can view units'),
        )

    def __unicode__(self):
        return self.shortname


class Tax(models.Model):
    taxrate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Taxrate in Percentage"))
    name = models.CharField(verbose_name=_("Taxname"), max_length=100)
    accountActiva = models.ForeignKey('accounting.Account', verbose_name=_("Activa Account"),
                                      related_name="db_relaccountactiva", null=True, blank=True)
    accountPassiva = models.ForeignKey('accounting.Account', verbose_name=_("Passiva Account"),
                                       related_name="db_relaccountpassiva", null=True, blank=True)

    def gettaxrate(self):
        return self.taxrate

    class Meta():
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')
        permissions = (
            ('view_tax', 'Can view tax rates'),
        )

    def __unicode__(self):
        return self.name


class Product(models.Model):
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    product_number = models.IntegerField(verbose_name=_("Product Number"))
    defaultunit = models.ForeignKey(Unit, verbose_name=_("Unit"))
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now_add=True)
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), null=True, blank="True")
    tax = models.ForeignKey(Tax, blank=False)
    accoutingProductCategorie = models.ForeignKey('accounting.ProductCategory',
                                                  verbose_name=_("Accounting Product Categorie"), null=True,
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
                                                                           customerGroupTransform.transform(
                                                                                   customerGroup),
                                                                           currency):
                            validpriceslist.append(price.price * customerGroup.factor)
                        else:
                            for unitTransfrom in list(unit_transforms):
                                if price.matches_date_unit_customer_group_currency(date,
                                                                                   unitTransfrom.transfrom(
                                                                                           unit).transform(
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
        return self.tax.gettaxrate()

    class Meta():
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        permissions = (
            ('view_product', 'Can view products'),
        )

    def __unicode__(self):
        return str(self.product_number) + ' ' + self.title

    class NoPriceFound(Exception):
        def __init__(self, customer, unit, date, product):
            self.customer = customer
            self.unit = unit
            self.date = date
            self.product = product
            return

        def __str__(self):
            return _("There is no Price for this product") + ": " + self.product.__unicode__() + _(
                "that matches the date") + ": " + self.date.__str__() + " ," + _(
                "customer") + ": " + self.customer.__unicode__() + _(" and unit") + ":" + self.unit.__unicode__()


class UnitTransform(models.Model):
    fromUnit = models.ForeignKey('Unit', verbose_name=_("From Unit"), related_name="db_reltransfromfromunit")
    toUnit = models.ForeignKey('Unit', verbose_name=_("To Unit"), related_name="db_reltransfromtounit")
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Unit"), blank=True, null=True)

    def transform(self, unit):
        if self.fromUnit == unit:
            return self.toUnit
        else:
            return unit

    class Meta():
        verbose_name = _('Unit Transfrom')
        verbose_name_plural = _('Unit Transfroms')

    def __unicode__(self):
        return "From " + self.fromUnit.shortname + " to " + self.toUnit.shortname


class CustomerGroupTransform(models.Model):
    fromCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name=_("From Unit"),
                                          related_name="db_reltransfromfromcustomergroup")
    toCustomerGroup = models.ForeignKey('CustomerGroup', verbose_name=_("To Unit"),
                                        related_name="db_reltransfromtocustomergroup")
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Customer Group"), blank=True, null=True)

    def transform(self, customer_group):
        if self.fromCustomerGroup == customer_group:
            return self.toCustomerGroup
        else:
            return customer_group

    def __unicode__(self):
        return "From " + self.fromCustomerGroup.name + " to " + self.toCustomerGroup.name

    class Meta():
        verbose_name = _('Customer Group Price Transfrom')
        verbose_name_plural = _('Customer Group Price Transfroms')


class Price(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"))
    unit = models.ForeignKey(Unit, blank=False, verbose_name=_("Unit"))
    currency = models.ForeignKey(Currency, blank=False, null=False, verbose_name='Currency')
    customerGroup = models.ForeignKey(CustomerGroup, blank=True, null=True, verbose_name=_("Customer Group"))
    price = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Price Per Unit"))
    validfrom = models.DateField(verbose_name=_("Valid from"), blank=True, null=True)
    validuntil = models.DateField(verbose_name=_("Valid until"), blank=True, null=True)

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
                if ((date - self.validuntil).days < 0) & (unit == self.unit) & (
                            self.customerGroup == customer_group) & (
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

    class Meta():
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')


class Position(models.Model):
    positionNumber = models.IntegerField(verbose_name=_("Position Number"))
    quantity = models.DecimalField(verbose_name=_("Quantity"), decimal_places=3, max_digits=10)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True,
                                   null=True)
    product = models.ForeignKey(Product, verbose_name=_("Product"), blank=True, null=True)
    unit = models.ForeignKey(Unit, verbose_name=_("Unit"), blank=True, null=True)
    sentOn = models.DateField(verbose_name=_("Shipment on"), blank=True, null=True)
    supplier = models.ForeignKey(Supplier, verbose_name=_("Shipment Supplier"),
                                 limit_choices_to={'direct_shipment_to_customers': True}, blank=True, null=True)
    shipmentID = models.CharField(max_length=100, verbose_name=_("Shipment ID"), blank=True, null=True)
    overwriteProductPrice = models.BooleanField(verbose_name=_('Overwrite Product Price'), default=False)
    positionPricePerUnit = models.DecimalField(verbose_name=_("Price Per Unit"), max_digits=17, decimal_places=2,
                                               blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2,
                                              verbose_name=_("Last Calculted Price"),
                                              blank=True, null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"),
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
            self.lastCalculatedTax = int(
                self.product.get_tax_rate() / 100 * self.positionPricePerUnit * self.quantity * (
                    1 - self.discount / 100) / currency.rounding) * currency.rounding
        else:
            self.lastCalculatedTax = self.product.get_tax_rate() / 100 * self.positionPricePerUnit * self.quantity
        self.save()
        return self.lastCalculatedTax

    def __unicode__(self):
        return _("Position") + ": " + str(self.id)

    class Meta():
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')


class SalesContractPosition(Position):
    contract = models.ForeignKey(SalesContract, verbose_name=_("Contract"))

    class Meta():
        verbose_name = _('Salescontract Position')
        verbose_name_plural = _('Salescontract Positions')

    def __unicode__(self):
        return _("Salescontract Position") + ": " + str(self.id)


class PurchaseOrderPosition(Position):
    contract = models.ForeignKey(PurchaseOrder, verbose_name=_("Contract"))

    class Meta():
        verbose_name = _('Purchaseorder Position')
        verbose_name_plural = _('Purchaseorder Positions')

    def __unicode__(self):
        return _("Purchaseorder Position") + ": " + str(self.id)


class XSLFile(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100, blank=True, null=True)
    xslfile = FileBrowseField(verbose_name=_("XSL File"), max_length=200)

    class Meta():
        verbose_name = _('XSL File')
        verbose_name_plural = _('XSL Files')

    def __unicode__(self):
        return self.title


class TemplateSet(models.Model):
    organisationname = models.CharField(verbose_name=_("Name of the Organisation"), max_length=200)
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    invoiceXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Invoice"),
                                       related_name="db_reltemplateinvoice")
    quoteXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Quote"), related_name="db_reltemplatequote")
    purchaseorderXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Purchaseorder"),
                                             related_name="db_reltemplatepurchaseorder")
    purchaseconfirmationXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Purchase Confirmation"),
                                                    related_name="db_reltemplatepurchaseconfirmation")
    deilveryorderXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Deilvery Order"),
                                             related_name="db_reltemplatedeliveryorder")
    profitLossStatementXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Profit Loss Statement"),
                                                   related_name="db_reltemplateprofitlossstatement")
    balancesheetXSLFile = models.ForeignKey(XSLFile, verbose_name=_("XSL File for Balancesheet"),
                                            related_name="db_reltemplatebalancesheet")
    logo = FileBrowseField(verbose_name=_("Logo for the PDF generation"), blank=True, null=True, max_length=200)
    bankingaccountref = models.CharField(max_length=60, verbose_name=_("Reference to Banking Account"), blank=True,
                                         null=True)
    addresser = models.CharField(max_length=200, verbose_name=_("Addresser"), blank=True, null=True)
    fopConfigurationFile = FileBrowseField(verbose_name=_("FOP Configuration File"), blank=True, null=True, max_length=200)
    footerTextsalesorders = models.TextField(verbose_name=_("Footer Text On Salesorders"), blank=True, null=True)
    headerTextsalesorders = models.TextField(verbose_name=_("Header Text On Salesorders"), blank=True, null=True)
    headerTextpurchaseorders = models.TextField(verbose_name=_("Header Text On Purchaseorders"), blank=True, null=True)
    footerTextpurchaseorders = models.TextField(verbose_name=_("Footer Text On Purchaseorders"), blank=True, null=True)
    pagefooterleft = models.CharField(max_length=40, verbose_name=_("Page Footer Left"), blank=True, null=True)
    pagefootermiddle = models.CharField(max_length=40, verbose_name=_("Page Footer Middle"), blank=True, null=True)

    class Meta():
        verbose_name = _('Templateset')
        verbose_name_plural = _('Templatesets')

    def __unicode__(self):
        return self.title


class UserExtension(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='avatars/', default='avatars/avatar.jpg', null=True, blank=True)
    defaultTemplateSet = models.ForeignKey(TemplateSet, null=True, blank=True)
    defaultCurrency = models.ForeignKey(Currency, null=True, blank=True)

    class Meta():
        verbose_name = _('User Extension')
        verbose_name_plural = _('User Extensions')

    def __unicode__(self):
        return self.user.__unicode__()