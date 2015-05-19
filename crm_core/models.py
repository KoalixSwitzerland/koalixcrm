# -*- coding: utf-8 -*-

from datetime import date, timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from filebrowser_safe.fields import FileBrowseField
from django_fsm import FSMIntegerField
from mezzanine.core.models import Displayable
from cartridge.shop import models as cartridge_models
from os import path
import reversion
from weasyprint import HTML
from international.models import countries, currencies, countries_raw
from const.postaladdressprefix import POSTAL_ADDRESS_PREFIX_CHOICES
from const.purpose import POSTAL_ADDRESS_PURPOSE_CHOICES, PHONE_ADDRESS_PURPOSE_CHOICES, EMAIL_ADDRESS_PURPOSE_CHOICES
from const.states import CONTRACT_STATE_CHOICES, CONTRACT_LABEL_CLASS_CHOICES
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


# ######################
# ##   Base Classes   ##
# ######################


class Contact(models.Model):
    prefix = models.CharField(max_length=1, choices=POSTAL_ADDRESS_PREFIX_CHOICES,
                              verbose_name=_("Title"), blank=True, null=True)
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True,
                                       verbose_name=_("Last modified by"), null=True)
    default_currency = models.CharField(max_length=3, choices=currencies, blank=True, null=True)

    @property
    def get_prefix(self):
        if self.prefix:
            for choice in POSTAL_ADDRESS_PREFIX_CHOICES:
                if self.prefix == choice[0]:
                    return choice[1]
        return ""

    @transaction.atomic()
    @reversion.create_revision()
    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.prefix:
            return "%s %s" % (self.get_prefix, self.name)
        return self.name


# #########################
# ##   Contact Related   ##
# #########################


class CustomerBillingCycle(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    days_to_payment = models.IntegerField(verbose_name=_("Days to Payment Date"))

    class Meta:
        verbose_name = _('Customer Billing Cycle')
        verbose_name_plural = _('Customer Billing Cycle')
        permissions = (
            ('view_customerbillingcycle', 'Can view billing cycles'),
        )

    def __unicode__(self):
        return self.name


class CustomerGroup(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Customer Group')
        verbose_name_plural = _('Customer Groups')
        permissions = (
            ('view_customer_group', 'Can view customer groups'),
        )


class PostalAddress(models.Model):
    addressline1 = models.CharField(max_length=200, verbose_name=_("Addressline 1"), blank=True, null=True)
    addressline2 = models.CharField(max_length=200, verbose_name=_("Addressline 2"), blank=True, null=True)
    zipcode = models.IntegerField(verbose_name=_("Zipcode"), blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name=_("City"), blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name=_("State"), blank=True, null=True)
    country = models.CharField(max_length=2, choices=countries, verbose_name=_("Country"), blank=True, null=True)
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=POSTAL_ADDRESS_PURPOSE_CHOICES,
                               default='C')
    person = models.ForeignKey(Contact, related_name='addresses')

    class Meta:
        verbose_name = _('Postal Address')
        verbose_name_plural = _('Postal Address')
        permissions = (
            ('view_postaladdress', 'Can view postal address'),
        )

    def get_purpose(self):
        for purpose in POSTAL_ADDRESS_PURPOSE_CHOICES:
            if self.purpose == purpose[0]:
                return purpose[1]
        return ""

    def get_country(self):
        return list(c[4].partition(',')[0].partition('(')[0].strip() for c in countries_raw if c[1] == self.country)[0]

    def __unicode__(self):
        if self.purpose and self.addressline1 and self.zipcode and self.city:
            return '%s: %s, %s %s' % (self.get_purpose(), self.addressline1, self.zipcode, self.city)
        elif self.addressline1 and self.zipcode and self.city:
            return '%s, %s %s' % (self.addressline1, self.zipcode, self.city)
        elif self.addressline1 and self.city:
            return '%s, %s' % (self.addressline1, self.city)
        elif self.zipcode and self.city:
            return '%s %s' % (self.zipcode, self.city)
        elif self.city:
            return unicode(self.city)
        return self.addressline1


class PhoneAddress(models.Model):
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PHONE_ADDRESS_PURPOSE_CHOICES,
                               default='H')
    person = models.ForeignKey(Contact, related_name='phonenumbers')

    class Meta:
        verbose_name = _('Phone Address')
        verbose_name_plural = _('Phone Address')
        permissions = (
            ('view_phoneaddress', 'Can view phone address'),
        )

    def get_purpose(self):
        for purpose in PHONE_ADDRESS_PURPOSE_CHOICES:
            if self.purpose == purpose[0]:
                return purpose[1]
        return ""

    def __unicode__(self):
        return "%s: %s" % (self.get_purpose(), self.phone)


class EmailAddress(models.Model):
    email = models.EmailField(max_length=200, verbose_name=_("Email Address"))
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=EMAIL_ADDRESS_PURPOSE_CHOICES,
                               default='H')
    person = models.ForeignKey(Contact, related_name='emailaddresses')

    class Meta:
        verbose_name = _('Email Address')
        verbose_name_plural = _('Email Address')
        permissions = (
            ('view_emailaddress', 'Can view email address'),
        )

    def get_purpose(self):
        for purpose in EMAIL_ADDRESS_PURPOSE_CHOICES:
            if self.purpose == purpose[0]:
                return purpose[1]
        return ""

    def __unicode__(self):
        return "%s: %s" % (self.get_purpose(), self.email)


# ########################
# ##    PARTICIPANTS    ##
# ########################


class Customer(Contact):
    firstname = models.CharField(max_length=300, verbose_name=_("Prename"), blank=True, null=True)
    billingcycle = models.ForeignKey(CustomerBillingCycle, verbose_name=_('Default Billing Cycle'))
    ismemberof = models.ManyToManyField(CustomerGroup, verbose_name=_('Is member of'), blank=True, null=True)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        permissions = (
            ('view_customer', 'Can view customers'),
        )

    def get_absolute_url(self):
        return reverse('customer_detail', args=[str(self.id)])

    def create_contract(self, request):
        contract = Contract()
        contract.default_customer = self
        contract.default_currency = self.default_currency
        contract.lastmodifiedby = request.user
        contract.staff = request.user
        contract.save()
        return contract

    def get_invoice_address(self):
        for address in self.addresses.all():
            if address.purpose == 'B':
                return address
            elif address.purpose == 'D':
                return address
            elif address.purpose == 'C':
                return address
        return "No Address"

    def get_quote_address(self):
        for address in self.addresses.all():
            if address.purpose == 'B':
                return address
            elif address.purpose == 'D':
                return address
            elif address.purpose == 'C':
                return address
        return "No Address"

    def get_contact_address(self):
        for address in self.addresses.all():
            if address.purpose == 'C':
                return address
            elif address.purpose == 'B':
                return address
            elif address.purpose == 'D':
                return address
        return "No Address"

    def get_phone_address(self):
        for pn in self.phonenumbers.all():
            if pn.purpose == 'O':
                return pn
            elif pn.purpose == 'B':
                return pn
            elif pn.purpose == 'H':
                return pn
            elif pn.purpose == 'P':
                return pn
        return "No Phone"

    def get_email_address(self):
        for ea in self.emailaddresses.all():
            if ea.purpose == 'O':
                return ea
            elif ea.purpose == 'H':
                return ea
        return "No email address"

    def create_invoice(self, request):
        contract = self.create_contract(request)
        invoice = contract.create_invoice()
        return invoice

    def create_purchase_order(self, request):
        contract = self.create_contract(request)
        purchase_order = contract.create_purchase_order()
        return purchase_order

    def create_quote(self, request):
        contract = self.create_contract(request)
        quote = contract.create_quote()
        return quote

    def is_in_group(self, customer_group):
        for customerGroupMembership in self.ismemberof.all():
            if customerGroupMembership.id == customer_group.id:
                return 1
        return 0

    def short_name(self):
        if self.firstname:
            return "%s %s" % (self.firstname, self.name)
        return self.name

    def __unicode__(self):
        if self.prefix and self.firstname:
            return "%s %s %s" % (self.get_prefix, self.firstname, self.name)
        else:
            return self.short_name()


class Supplier(Contact):
    direct_shipment_to_customers = models.BooleanField(verbose_name=_("Offers direct Shipment to Customer"),
                                                       default=False)

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")
        permissions = (
            ('view_supplier', 'Can view suppliers'),
        )

    def get_absolute_url(self):
        return reverse('supplier_detail', args=[str(self.id)])

    def __unicode__(self):
        if self.prefix:
            return "%s %s" % (self.get_prefix, self.name)
        return self.name


# ##########################
# ##   CONTRACT RELATED   ##
# ##########################


class Contract(models.Model):
    state = FSMIntegerField(default=10, choices=CONTRACT_STATE_CHOICES)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True,
                              verbose_name=_("Staff"), related_name="db_relcontractstaff", null=True)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    default_customer = models.ForeignKey(Customer, verbose_name=_("Default Customer"), null=True, blank=True)
    default_supplier = models.ForeignKey(Supplier, verbose_name=_("Default Supplier"), null=True, blank=True)
    default_currency = models.CharField(max_length=3, choices=currencies, verbose_name=_("Default Currency"),
                                        blank=True, null=True)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_contractlstmodified",
                                       null=True)

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')
        permissions = (
            ('view_contract', 'Can view contracts'),
        )
        get_latest_by = 'lastmodification'

    def get_price(self):
        res = "N/A"
        if self.has_quotes() and not self.has_invoices() and not self.has_purchaseorders():
            res = str(self.quotes.last().get_price()) + " " + self.default_currency
        elif self.has_purchaseorders() and not self.has_invoices():
            res = str(self.purchaseorders.last().get_price()) + " " + self.default_currency
        elif self.has_invoices():
            res = str(self.invoices.last().get_price()) + " " + self.default_currency
        return res

    def create_invoice(self):
        invoice = Invoice()
        invoice.contract = self
        invoice.discount = 0
        invoice.staff = self.staff
        invoice.customer = self.default_customer
        invoice.status = 1
        invoice.currency = self.default_currency
        invoice.payableuntil = date.today() + timedelta(days=self.default_customer.billingcycle.days_to_payment)
        invoice.dateofcreation = date.today().__str__()
        invoice.save()
        self.state = 30
        self.save()
        return invoice

    def create_quote(self):
        quote = Quote()
        quote.contract = self
        quote.discount = 0
        quote.staff = self.staff
        quote.customer = self.default_customer
        quote.status = 1
        quote.currency = self.default_currency
        quote.validuntil = date.today()
        quote.dateofcreation = date.today()
        quote.save()
        self.state = 50
        self.save()
        return quote

    def create_purchase_order(self):
        purchaseorder = PurchaseOrder()
        purchaseorder.contract = self
        purchaseorder.customer = self.default_customer
        purchaseorder.description = self.description
        purchaseorder.discount = 0
        purchaseorder.currency = self.default_currency
        purchaseorder.supplier = self.default_supplier
        purchaseorder.status = 1
        purchaseorder.dateofcreation = date.today()
        purchaseorder.save()
        self.state = 70
        self.save()
        return purchaseorder

    def get_name(self):
        return _('Contract') + ' #' + str(self.id)

    def get_state(self):
        for state in CONTRACT_STATE_CHOICES:
            if self.state == state[0]:
                return state[1]
        return "Unknown"

    def get_state_class(self):
        for state in CONTRACT_LABEL_CLASS_CHOICES:
            if self.state == state[0]:
                return state[1]
        return "default"

    def get_absolute_url(self):
        url = '/contracts/detail/' + str(self.pk)  # TODO: Bad solution
        return url

    def get_quote_detail_url(self):
        return self.quotes.latest().get_document_url()

    def get_quote_edit_url(self):
        return self.quotes.latest().get_absolute_url()

    def get_purchaseorder_detail_url(self):
        return self.purchaseorders.latest().get_document_url()

    def get_purchaseorder_edit_url(self):
        return self.purchaseorders.latest().get_absolute_url()

    def get_invoice_detail_url(self):
        return self.invoices.latest().get_document_url()

    def get_invoice_edit_url(self):
        return self.invoices.latest().get_absolute_url()

    def has_quotes(self):
        return bool(self.quotes.count() > 0)

    def has_purchaseorders(self):
        return bool(self.purchaseorders.count() > 0)

    def has_invoices(self):
        return bool(self.invoices.count() > 0)

    def __unicode__(self):
        return self.get_name()


class PurchaseOrder(models.Model):
    contract = models.ForeignKey(Contract, verbose_name=_("Contract"), related_name='purchaseorders')
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"))
    external_reference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, verbose_name=_("Supplier"), blank=True, null=True)
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    last_pricing_date = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    last_calculated_price = models.DecimalField(max_digits=17, decimal_places=2,
                                                verbose_name=_("Last Calculated Price With Tax"), blank=True, null=True)
    last_calculated_tax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculated Tax"),
                                              blank=True, null=True)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True,
                              verbose_name=_("Staff"), related_name="db_relpostaff", null=True)
    currency = models.CharField(max_length=3, choices=currencies, verbose_name=_("Currency"), blank=False, null=False)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_polstmodified", null=True,
                                       blank=True)
    derived_from_quote = models.ForeignKey('Quote', related_name='purchaseorders', null=True, blank=True)
    pdf_path = models.CharField(max_length=200, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Order')
        permissions = (
            ('view_purchaseorder', 'Can view purchase orders'),
        )
        get_latest_by = 'lastmodification'

    def get_price(self):
        return 10

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
            self.last_calculated_price = price
            self.last_calculated_tax = tax
            self.last_pricing_date = pricing_date
            return 1
        except Quote.DoesNotExist, e:
            print "ERROR " + e.__str__()
            print "Der Fehler trat beim File: " + self.sourcefile
            exit()
            return 0

    def to_html(self):
        return render_to_string('pdf_templates/purchaseorder.html', {'purchaseorder': self})

    def create_pdf(self):
        html = self.to_html()
        pth = path.normpath('%s/%s/uploads/pdf/purchaseorders/purchaseorder-%s.pdf' % (
            settings.PROJECT_ROOT, settings.MEDIA_URL, self.pk))
        self.pdf_path = pth
        HTML(string=html, encoding="utf8").write_pdf(target=pth)

    def get_absolute_url(self):
        return reverse('purchaseorder_edit', args=[str(self.id)])

    def get_document_url(self):
        return reverse('purchaseorder_detail', args=[str(self.id)])

    @transaction.atomic()
    @reversion.create_revision()
    def save(self, *args, **kwargs):
        # self.recalculate_prices(date.today())
        super(PurchaseOrder, self).save(*args, **kwargs)
        self.create_pdf()
        super(PurchaseOrder, self).save(*args, **kwargs)

    def __unicode__(self):
        return _("Purchase Order") + " #" + str(self.id)


class SalesContract(models.Model):
    external_reference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    description = models.CharField(verbose_name=_("Description"), max_length=100, blank=True, null=True)
    last_pricing_date = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True, editable=False)
    last_calculated_price = models.DecimalField(max_digits=17, decimal_places=2,
                                                verbose_name=_("Last Calculated Price With Tax"),
                                                blank=True, null=True, editable=False)
    last_calculated_tax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculated Tax"),
                                              blank=True, null=True, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"))
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True,
                              verbose_name=_("Staff"), related_name="db_relscstaff", null=True)
    currency = models.CharField(max_length=3, choices=currencies, verbose_name=_("Currency"), blank=False, null=False)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"), editable=False)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"), editable=False)
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_lstscmodified", null=True,
                                       blank="True", editable=False)
    pdf_path = models.CharField(max_length=200, null=True, blank=True, editable=False)

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

            self.last_calculated_price = price
            self.last_calculated_tax = tax
            self.last_pricing_date = pricing_date
            return 1
        except SalesContract.DoesNotExist:
            return 0

    # TODO
    @transaction.atomic()
    @reversion.create_revision()
    def save(self, *args, **kwargs):
        # self.recalculate_prices(date.today())
        super(SalesContract, self).save(*args, **kwargs)


class Quote(SalesContract):
    contract = models.ForeignKey(Contract, verbose_name=_('Contract'), related_name='quotes')
    validuntil = models.DateField(verbose_name=_("Valid until"))

    class Meta:
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')
        permissions = (
            ('view_quote', 'Can view quotes'),
        )
        get_latest_by = "lastmodification"

    def get_price(self):
        return 20

    def create_invoice(self):
        invoice = Invoice()
        invoice.contract = self.contract
        invoice.description = self.description
        invoice.discount = self.discount
        invoice.customer = self.customer
        invoice.staff = self.staff
        invoice.status = 10
        invoice.derived_from_quote = self
        invoice.currency = self.currency
        invoice.payableuntil = date.today() + timedelta(
            days=self.customer.billingcycle.days_to_payment)
        invoice.dateofcreation = date.today().__str__()
        invoice.customerBillingCycle = self.customer.billingcycle
        invoice.save()
        self.save()
        try:
            quote_positions = SalesContractPosition.objects.filter(contract=self.id)
            for quotePosition in list(quote_positions):
                invoice_position = SalesContractPosition()
                invoice_position.product = quotePosition.product
                invoice_position.position_number = quotePosition.positionNumber
                invoice_position.quantity = quotePosition.quantity
                invoice_position.description = quotePosition.description
                invoice_position.discount = quotePosition.discount
                invoice_position.product = quotePosition.product
                invoice_position.unit = quotePosition.unit
                invoice_position.sent_on = quotePosition.sentOn
                invoice_position.supplier = quotePosition.supplier
                invoice_position.shipment_id = quotePosition.shipmentID
                invoice_position.overwrite_product_price = quotePosition.overwriteProductPrice
                invoice_position.position_price_per_unit = quotePosition.positionPricePerUnit
                invoice_position.last_pricing_date = quotePosition.lastPricingDate
                invoice_position.last_calculated_price = quotePosition.lastCalculatedPrice
                invoice_position.last_calculated_tax = quotePosition.lastCalculatedTax
                invoice_position.contract = invoice
                invoice_position.save()
            return invoice
        except Quote.DoesNotExist:
            return

    def create_purchase_order(self):
        purchase_order = self.contract.create_purchase_order()
        self.save()
        return purchase_order

    def to_html(self):
        return render_to_string('pdf_templates/quote.html', {'quote': self})

    def create_pdf(self):
        html = self.to_html()
        pth = path.normpath('%s/%s/uploads/pdf/quotes/quote-%s.pdf' % (
            settings.PROJECT_ROOT, settings.MEDIA_URL, self.pk))
        self.pdf_path = pth
        HTML(string=html, encoding="utf8").write_pdf(target=pth)

    def get_absolute_url(self):
        return reverse('quote_edit', args=[str(self.id)])

    def get_document_url(self):
        return reverse('quote_detail', args=[str(self.id)])

    def __unicode__(self):
        return _('Quote') + ' #' + str(self.id)

    @transaction.atomic()
    @reversion.create_revision()
    def save(self, *args, **kwargs):
        super(Quote, self).save(*args, **kwargs)
        self.create_pdf()
        super(Quote, self).save(*args, **kwargs)


class Invoice(SalesContract):
    contract = models.ForeignKey(Contract, verbose_name=_('Contract'), related_name='invoices')
    payableuntil = models.DateField(verbose_name=_("To pay until"))
    derived_from_quote = models.ForeignKey(Quote, blank=True, null=True, editable=False)
    payment_bank_reference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                              null=True)

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        permissions = (
            ('view_invoice', 'Can view invoices'),
        )
        get_latest_by = 'lastmodification'

    def get_price(self):
        return 30

    def to_html(self):
        return render_to_string('pdf_templates/invoice.html', {'invoice': self})

    def create_pdf(self):
        html = self.to_html()
        pth = path.normpath('%s/%s/uploads/pdf/invoices/invoice-%s.pdf' % (
            settings.PROJECT_ROOT, settings.MEDIA_URL, self.pk))
        self.pdf_path = pth
        HTML(string=html, encoding="utf8").write_pdf(target=pth)

    def get_absolute_url(self):
        return reverse('invoice_edit', args=[str(self.id)])

    def get_document_url(self):
        return reverse('invoice_detail', args=[str(self.id)])

    def __unicode__(self):
        return _("Invoice") + " #" + str(self.id)

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)
        self.create_pdf()
        super(Invoice, self).save(*args, **kwargs)


class Unit(models.Model):
    description = models.CharField(verbose_name=_("Description"), max_length=100)
    shortname = models.CharField(verbose_name=_("Displayed Name After Quantity In The Position"), max_length=3)
    fractionof = models.ForeignKey('self', blank=True, null=True, verbose_name=_("Is A Fraction Of"))
    factor = models.IntegerField(verbose_name=_("Factor Between This And Next Higher Unit"),
                                 blank=True, null=True)

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        permissions = (
            ('view_unit', 'Can view units'),
        )

    def __unicode__(self):
        return self.shortname


class TaxRate(models.Model):
    taxrate_in_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Taxrate in Percentage"))
    name = models.CharField(verbose_name=_("Taxname"), max_length=100)

    # TODO
    def gettaxrate(self):
        return self.taxrate_in_percent

    class Meta:
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')
        permissions = (
            ('view_tax', 'Can view tax rates'),
        )

    def __unicode__(self):
        return self.name


class ProductCategory(cartridge_models.Category):

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')

    def __unicode__(self):
        return self.title


class ProductItem(cartridge_models.Product):
    item_unit = models.ForeignKey(Unit, verbose_name=_("Unit"))
    item_tax = models.ForeignKey(TaxRate, blank=False)
    item_category = models.ForeignKey(ProductCategory, verbose_name=_("Product Categorie"), null=True, blank=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        permissions = (
            ('view_product', 'Can view products'),
        )

    def get_price(self):
        return self.price()

    def get_tax_rate(self):
        return self.item_tax.gettaxrate()

    def __unicode__(self):
        return '%s (#%s)' % (self.title, str(self.pk))


class UnitTransform(models.Model):
    from_unit = models.ForeignKey(Unit, verbose_name=_("From Unit"), related_name="db_reltransformfromunit")
    to_unit = models.ForeignKey(Unit, verbose_name=_("To Unit"), related_name="db_reltransformtounit")
    product = models.ForeignKey(ProductItem, verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Unit"), blank=True, null=True)

    def transform(self, unit):
        if self.from_unit == unit:
            return self.to_unit
        else:
            return unit

    class Meta:
        verbose_name = _('Unit Transform')
        verbose_name_plural = _('Unit Transforms')

    def __unicode__(self):
        return "From " + self.from_unit.shortname + " to " + self.to_unit.shortname


class Position(models.Model):
    position_number = models.IntegerField(verbose_name=_("Position Number"), default=0)
    quantity = models.DecimalField(verbose_name=_("Quantity"), decimal_places=3, max_digits=10)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    product = models.ForeignKey(ProductItem, verbose_name=_("Product"), blank=True, null=True)
    unit = models.ForeignKey(Unit, verbose_name=_("Unit"), blank=True, null=True)
    sent_on = models.DateField(verbose_name=_("Shipment on"), blank=True, null=True)
    supplier = models.ForeignKey(Supplier, verbose_name=_("Shipment Supplier"),
                                 limit_choices_to={'direct_shipment_to_customers': True}, blank=True, null=True)
    shipment_id = models.CharField(max_length=100, verbose_name=_("Shipment ID"), blank=True, null=True)
    overwrite_product_price = models.BooleanField(verbose_name=_('Overwrite Product Price'), default=False)
    position_price_per_unit = models.DecimalField(verbose_name=_("Price Per Unit"), max_digits=17, decimal_places=2,
                                                  blank=True, null=True)
    last_pricing_date = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    last_calculated_price = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculated Price"),
                                                blank=True, null=True)
    last_calculated_tax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculated Tax"),
                                              blank=True, null=True)

    def recalculate_prices(self, pricing_date, customer, currency):
        if not self.overwrite_product_price:
            self.position_price_per_unit = self.product.get_price()
        if type(self.discount) == Decimal:
            self.last_calculated_price = int(self.position_price_per_unit * self.quantity * (
                1 - self.discount / 100) / currency.rounding) * currency.rounding
        else:
            self.last_calculated_price = self.position_price_per_unit * self.quantity
        self.last_pricing_date = pricing_date
        self.save()
        return self.last_calculated_price

    def recalculate_tax(self, currency):
        if type(self.discount) == Decimal:
            self.last_calculated_tax = int(
                self.product.get_tax_rate() / 100 * self.position_price_per_unit * self.quantity * (
                    1 - self.discount / 100) / currency.rounding) * currency.rounding
        else:
            self.last_calculated_tax = self.product.get_tax_rate() / 100 * self.position_price_per_unit * self.quantity
        self.save()
        return self.last_calculated_tax

    def __unicode__(self):
        return _("Position") + ": " + str(self.id)

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')


class SalesContractPosition(Position):
    contract = models.ForeignKey(SalesContract, verbose_name=_("Contract"), related_name='positions')

    class Meta:
        verbose_name = _('Salescontract Position')
        verbose_name_plural = _('Salescontract Positions')

    def __unicode__(self):
        return _("Salescontract Position") + ": " + str(self.id)


class PurchaseOrderPosition(Position):
    contract = models.ForeignKey(PurchaseOrder, verbose_name=_("Contract"))

    class Meta:
        verbose_name = _('Purchaseorder Position')
        verbose_name_plural = _('Purchaseorder Positions')

    def __unicode__(self):
        return _("Purchaseorder Position") + ": " + str(self.id)


class HTMLFile(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100, blank=True, null=True)
    file = FileBrowseField(verbose_name=_("HTML File"), max_length=200)

    class Meta:
        verbose_name = _('HTML File')
        verbose_name_plural = _('HTML Files')

    def __unicode__(self):
        return self.title


class TemplateSet(models.Model):
    organisationname = models.CharField(verbose_name=_("Name of the Organisation"), max_length=200)
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    invoice_html_file = models.ForeignKey(HTMLFile, verbose_name=_("HTML File for Invoice"),
                                          related_name="invoice_template")
    quote_html_file = models.ForeignKey(HTMLFile, verbose_name=_("HTML File for Quote"), related_name="quote_template")
    purchaseorder_html_file = models.ForeignKey(HTMLFile, verbose_name=_("HTML File for Purchaseorder"),
                                                related_name="purchaseorder_template")
    logo = FileBrowseField(verbose_name=_("Logo"), blank=True, null=True, max_length=200)
    addresser = models.CharField(max_length=200, verbose_name=_("Addresser"), blank=True, null=True)
    footer_text_salesorders = models.TextField(verbose_name=_("Footer Text On Salesorders"), blank=True, null=True)
    header_text_salesorders = models.TextField(verbose_name=_("Header Text On Salesorders"), blank=True, null=True)
    header_text_purchaseorders = models.TextField(verbose_name=_("Header Text On Purchaseorders"), blank=True,
                                                  null=True)
    footer_text_purchaseorders = models.TextField(verbose_name=_("Footer Text On Purchaseorders"), blank=True,
                                                  null=True)
    page_footer_left = models.CharField(max_length=40, verbose_name=_("Page Footer Left"), blank=True, null=True)
    page_footer_middle = models.CharField(max_length=40, verbose_name=_("Page Footer Middle"), blank=True, null=True)

    class Meta:
        verbose_name = _('Templateset')
        verbose_name_plural = _('Templatesets')

    def __unicode__(self):
        return self.title


class UserExtension(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='extension')
    image = models.ImageField(upload_to='avatars/', default='avatars/avatar.jpg', null=True, blank=True)
    default_templateset = models.ForeignKey(TemplateSet, null=True, blank=True)
    default_currency = models.CharField(max_length=3, choices=currencies, null=True, blank=True)

    class Meta:
        verbose_name = _('User Extension')
        verbose_name_plural = _('User Extensions')

    def __unicode__(self):
        return self.user.__unicode__()