# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime
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
from const.postaladdressprefix import POSTAL_ADDRESS_PREFIX_CHOICES, PostalAddressPrefix
from const.purpose import POSTAL_ADDRESS_PURPOSE_CHOICES, PHONE_ADDRESS_PURPOSE_CHOICES, \
    EMAIL_ADDRESS_PURPOSE_CHOICES, EmailAddressPurpose, PhoneAddressPurpose, PostalAddressPurpose
from const.states import CONTRACT_STATE_CHOICES, ContractStatesEnum, ContractStatesLabelEnum
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from solo.models import SingletonModel


# ######################
# ##   Base Classes   ##
# ######################

class Contact(models.Model):
    prefix = models.CharField(
        max_length=1, choices=POSTAL_ADDRESS_PREFIX_CHOICES, verbose_name=_("Title"), blank=True, null=True)
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), null=True)
    default_currency = models.CharField(
        verbose_name=_('Currency'), max_length=3, choices=currencies, blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def get_prefix(self):
        if self.prefix:
            return PostalAddressPrefix.choices[self.prefix]
        return ""

    @transaction.atomic()
    @reversion.create_revision()
    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.prefix:
            return "%s %s" % (self.get_prefix, self.name)
        return self.name


class EmailAddress(models.Model):
    email = models.EmailField(max_length=200, verbose_name=_("Email Address"))
    purpose = models.CharField(
        verbose_name=_("Purpose"), max_length=1, choices=EMAIL_ADDRESS_PURPOSE_CHOICES, default='H')

    class Meta:
        abstract = True
        verbose_name = _('Email Address')
        verbose_name_plural = _('Email Address')
        permissions = (
            ('view_emailaddress', 'Can view email address'),
        )

    def get_purpose(self):
        return EmailAddressPurpose.choices[self.purpose]

    def __unicode__(self):
        return "%s" % self.email


class PhoneAddress(models.Model):
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    purpose = models.CharField(
        verbose_name=_("Purpose"), max_length=1, choices=PHONE_ADDRESS_PURPOSE_CHOICES, default='H')

    class Meta:
        abstract = True
        verbose_name = _('Phone Address')
        verbose_name_plural = _('Phone Address')
        permissions = (
            ('view_phoneaddress', 'Can view phone address'),
        )

    def get_purpose(self):
        return PhoneAddressPurpose.choices[self.purpose]

    def __unicode__(self):
        return "%s" % self.phone


class PostalAddress(models.Model):
    addressline1 = models.CharField(max_length=200, verbose_name=_("Addressline 1"), blank=True, null=True)
    addressline2 = models.CharField(max_length=200, verbose_name=_("Addressline 2"), blank=True, null=True)
    zipcode = models.IntegerField(verbose_name=_("Zipcode"), blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name=_("City"), blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name=_("State"), blank=True, null=True)
    country = models.CharField(max_length=2, choices=countries, verbose_name=_("Country"), blank=True, null=True)
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=POSTAL_ADDRESS_PURPOSE_CHOICES,
                               default='C')

    class Meta:
        abstract = True
        verbose_name = _('Postal Address')
        verbose_name_plural = _('Postal Address')
        permissions = (
            ('view_postaladdress', 'Can view postal address'),
        )

    def get_purpose(self):
        return PostalAddressPurpose.choices[self.purpose]

    def get_country(self):
        return list(c[4].partition(',')[0].partition('(')[0].strip() for c in countries_raw if c[1] == self.country)[0]

    def __unicode__(self):
        if self.addressline1 and self.zipcode and self.city:
            return '%s, %s %s' % (self.addressline1, self.zipcode, self.city)
        elif self.addressline1 and self.city:
            return '%s, %s' % (self.addressline1, self.city)
        elif self.zipcode and self.city:
            return '%s %s' % (self.zipcode, self.city)
        elif self.city:
            return unicode(self.city)
        return self.addressline1


class SalesContract(models.Model):
    external_reference = models.CharField(verbose_name=_("External Reference"), max_length=100, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    customer = models.ForeignKey('crm_core.Customer', verbose_name=_("Customer"))
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"), editable=False)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"), editable=False)
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True,
                                       verbose_name=_("Last modified by"), null=True)
    pdf_path = models.CharField(max_length=200, null=True, blank=True, editable=False)

    class Meta:
        abstract = True

    @transaction.atomic()
    @reversion.create_revision()
    def save(self, *args, **kwargs):
        super(SalesContract, self).save(*args, **kwargs)


# #############################
# ## CARTRIDGE MODIFICATIONS ##
# #############################

class CustomerCartItem(cartridge_models.CartItem):
    product = models.ForeignKey(cartridge_models.Product, verbose_name=_('Product'))

    def save(self, *args, **kwargs):
        self.sku = self.product.sku
        self.unit_price = self.product.price()
        self.url = self.product.get_absolute_url()
        super(CustomerCartItem, self).save(*args, **kwargs)

CustomerCartItem._meta.get_field('description').blank = True


# ########################
# ##    PARTICIPANTS    ##
# ########################

class Customer(Contact, Displayable):
    firstname = models.CharField(max_length=300, verbose_name=_("Prename"), blank=True, null=True)
    billingcycle = models.ForeignKey('crm_core.CustomerBillingCycle', verbose_name=_('Billing Cycle'))
    ismemberof = models.ManyToManyField('crm_core.CustomerGroup', verbose_name=_('Is member of'), blank=True)
    search_fields = ('firstname', 'name')

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


class Supplier(Contact, Displayable):
    direct_shipment_to_customers = models.BooleanField(verbose_name=_("Offers direct Shipment to Customer"),
                                                       default=False)
    search_fields = ('name', )

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


# #########################
# ##   Contact Related   ##
# #########################

class CustomerPostalAddress(PostalAddress):
    person = models.ForeignKey(Customer, related_name='addresses')


class SupplierPostalAddress(PostalAddress):
    person = models.ForeignKey(Supplier, related_name='addresses')


class CustomerPhoneAddress(PhoneAddress):
    person = models.ForeignKey(Customer, related_name='phonenumbers')


class SupplierPhoneAddress(PhoneAddress):
    person = models.ForeignKey(Supplier, related_name='phonenumbers')


class CustomerEmailAddress(EmailAddress):
    person = models.ForeignKey(Customer, related_name='emailaddresses')


class SupplierEmailAddress(EmailAddress):
    person = models.ForeignKey(Supplier, related_name='emailaddresses')


class CustomerBillingCycle(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    days_to_payment = models.IntegerField(verbose_name=_("Days to Payment Date"))
    prefix = models.CharField(max_length=300, verbose_name=_("Prefix"), null=True)

    class Meta:
        verbose_name = _('Billing Cycle')
        verbose_name_plural = _('Billing Cycles')
        permissions = (
            ('view_customerbillingcycle', 'Can view billing cycles'),
        )

    def __unicode__(self):
        return "%s %s" % (self.prefix, self.name)


class CustomerGroup(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=300)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Customer Group')
        verbose_name_plural = _('Customer Groups')
        permissions = (
            ('view_customer_group', 'Can view customer groups'),
        )


# ##########################
# ##   CONTRACT RELATED   ##
# ##########################


class Contract(Displayable):
    state = FSMIntegerField(default=10, choices=CONTRACT_STATE_CHOICES)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True,
                              verbose_name=_("Staff"), related_name="db_relcontractstaff", null=True)
    default_customer = models.ForeignKey(Customer, verbose_name=_("Default Customer"), null=True, blank=True)
    default_supplier = models.ForeignKey(Supplier, verbose_name=_("Default Supplier"), null=True, blank=True)
    default_currency = models.CharField(max_length=3, choices=currencies, verbose_name=_("Currency"),
                                        blank=True, null=True)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), related_name="db_contractlstmodified",
                                       null=True)
    search_fields = ('title', 'description', )

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')
        permissions = (
            ('view_contract', 'Can view contracts'),
        )
        get_latest_by = 'lastmodification'

    # ToDo refs #67
    def get_price(self):
        res = "N/A"
        if self.has_quotes() and not self.has_invoices() and not self.has_purchaseorders():
            res = str(self.quotes.last().get_price())
        elif self.has_purchaseorders() and not self.has_invoices():
            res = str(self.purchaseorders.last().get_price())
        elif self.has_invoices():
            res = str(self.invoices.last().get_price())
        return res

    def create_invoice(self):
        invoice = Invoice(
            contract=self,
            customer=self.default_customer,
            payableuntil=date.today() + timedelta(days=self.default_customer.billingcycle.days_to_payment)
        )
        invoice.discount = 0
        invoice.staff = self.staff
        invoice.cart = self.purchaseorders.latest().cart
        invoice.save()
        return invoice

    def create_quote(self):
        quote = Quote(contract=self, customer=self.default_customer)
        quote.discount = 0
        quote.staff = self.staff
        quote.status = 1
        quote.validuntil = date.today() + timedelta(days=self.default_customer.billingcycle.days_to_payment)
        quote.save()
        return quote

    def create_purchase_order(self):
        purchaseorder = PurchaseOrder(contract=self, customer=self.default_customer)
        purchaseorder.description = self.description
        purchaseorder.discount = 0
        purchaseorder.staff = self.staff
        purchaseorder.supplier = self.default_supplier
        purchaseorder.status = 1
        if self.quotes.count() > 0:
            purchaseorder.cart = self.quotes.latest().cart
        purchaseorder.save()
        return purchaseorder

    def get_name(self):
        return _('Contract') + ' #' + str(self.id)

    def get_state(self):
        return ContractStatesEnum.choices[self.state]

    def get_state_class(self):
        return ContractStatesLabelEnum.choices[self.state]

    def get_absolute_url(self):
        return reverse('contract_detail', args=[str(self.pk)])

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


class PurchaseOrder(SalesContract, Displayable):
    contract = models.ForeignKey(Contract, verbose_name=_("Contract"), related_name='purchaseorders')
    validuntil = models.DateField(verbose_name=_("Valid until"), null=True)
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"), null=True,
        related_name='purchaseorder_staff')
    cart = models.ForeignKey(cartridge_models.Cart, null=True)
    search_fields = ('title', 'description', )

    class Meta:
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Order')
        permissions = (
            ('view_purchaseorder', 'Can view purchase orders'),
        )
        get_latest_by = 'lastmodification'

    def __init__(self, *args, **kwargs):
        super(PurchaseOrder, self).__init__(*args, **kwargs)
        if not self.cart:
            cart = cartridge_models.Cart()
            cart.save()
            self.cart = cart
            self.save()

    def to_html(self):
        crtitems = []
        for itm in self.cart.items.all():
            crtitems.append(CustomerCartItem.objects.get(cartitem_ptr_id=itm.id))
        company_data = CompanyContactData.objects.get(pk=1)
        customer = self.customer
        return render_to_string('pdf_templates/purchaseorder.html',
                                {
                                    'purchaseorder': self,
                                    'positions': crtitems,
                                    'company_data': company_data,
                                    'customer': customer
                                })

    def create_pdf(self):
        html = self.to_html()
        pth = path.normpath('%s/%s/data/pdf/purchaseorders/purchaseorder-%s.pdf' % (
            settings.PROJECT_ROOT, settings.MEDIA_URL, self.pk))
        self.pdf_path = pth
        HTML(string=html, encoding="utf8").write_pdf(target=pth)

    def get_absolute_url(self):
        return reverse('purchaseorder_edit', args=[str(self.id)])

    def get_document_url(self):
        return reverse('purchaseorder_detail', args=[str(self.id)])

    def get_price(self):
        return "%s %s" % (self.cart.total_price(), self.contract.default_currency)

    def __unicode__(self):
        return _("Purchase Order") + " #" + str(self.id)

    @transaction.atomic()
    @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.cart.last_updated = datetime.now()
        self.cart.save()
        super(PurchaseOrder, self).save(*args, **kwargs)
        self.contract.state = 70
        self.contract.save()
        self.create_pdf()


class Quote(SalesContract, Displayable):
    contract = models.ForeignKey(Contract, verbose_name=_('Contract'), related_name='quotes')
    validuntil = models.DateField(verbose_name=_("Valid until"), null=True)
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True, verbose_name=_("Staff"),
        null=True, related_name="quote_staff")
    cart = models.ForeignKey(cartridge_models.Cart, null=True)
    search_fields = ('title', 'description', )

    class Meta:
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')
        permissions = (
            ('view_quote', 'Can view quotes'),
        )
        get_latest_by = "lastmodification"

    def __init__(self, *args, **kwargs):
        super(Quote, self).__init__(*args, **kwargs)
        if not self.cart:
            cart = cartridge_models.Cart()
            cart.save()
            self.cart = cart
            self.save()

    def create_invoice(self):
        invoice = Invoice()
        invoice.contract = self.contract
        invoice.description = self.description
        invoice.discount = self.discount
        invoice.customer = self.customer
        invoice.staff = self.staff
        invoice.status = 10
        invoice.derived_from_quote = self
        invoice.payableuntil = date.today() + timedelta(
            days=self.customer.billingcycle.days_to_payment)
        invoice.customerBillingCycle = self.customer.billingcycle
        invoice.save()
        self.save()
        return

    def create_purchase_order(self):
        purchase_order = self.contract.create_purchase_order()
        self.save()
        return purchase_order

    def to_html(self):
        crtitems = []
        for itm in self.cart.items.all():
            crtitems.append(CustomerCartItem.objects.get(cartitem_ptr_id=itm.id))
        company_data = CompanyContactData.objects.get(pk=1)
        customer = self.customer
        return render_to_string('pdf_templates/quote.html',
                                {
                                    'quote': self,
                                    'positions': crtitems,
                                    'company_data': company_data,
                                    'customer': customer
                                })

    def create_pdf(self):
        html = self.to_html()
        pth = path.normpath('%s/%s/data/pdf/quotes/quote-%s.pdf' % (
            settings.PROJECT_ROOT, settings.MEDIA_URL, self.pk))
        self.pdf_path = pth
        HTML(string=html, encoding="utf8").write_pdf(target=pth)

    def get_absolute_url(self):
        return reverse('quote_edit', args=[str(self.id)])

    def get_document_url(self):
        return reverse('quote_detail', args=[str(self.id)])

    def get_price(self):
        return "%s %s" % (self.cart.total_price(), self.contract.default_currency)

    def __unicode__(self):
        return _('Quote') + ' #' + str(self.id)

    @transaction.atomic()
    @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.cart.last_updated = datetime.now()
        self.cart.save()
        super(Quote, self).save(*args, **kwargs)
        self.contract.state = 50
        self.contract.save()
        self.create_pdf()


class Invoice(SalesContract, Displayable):
    contract = models.ForeignKey(Contract, verbose_name=_('Contract'), related_name='invoices')
    payableuntil = models.DateField(verbose_name=_("To pay until"))
    payment_bank_reference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                              null=True)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, blank=True,
                              verbose_name=_("Staff"), related_name="db_relscstaff", null=True)
    cart = models.ForeignKey(cartridge_models.Cart, null=True)
    search_fields = ('title', 'description', )

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        permissions = (
            ('view_invoice', 'Can view invoices'),
        )
        get_latest_by = 'lastmodification'

    def __init__(self, *args, **kwargs):
        super(Invoice, self).__init__(*args, **kwargs)
        if not self.cart:
            cart = cartridge_models.Cart()
            cart.save()
            self.cart = cart
            self.save()

    def to_html(self):
        crtitems = []
        for itm in self.cart.items.all():
            crtitems.append(CustomerCartItem.objects.get(cartitem_ptr_id=itm.id))
        company_data = CompanyContactData.objects.get(pk=1)
        customer = self.customer
        return render_to_string('pdf_templates/invoice.html',
                                {
                                    'invoice': self,
                                    'positions': crtitems,
                                    'company_data': company_data,
                                    'customer': customer
                                })

    def create_pdf(self):
        html = self.to_html()
        pth = path.normpath('%s/%s/data/pdf/invoices/invoice-%s.pdf' % (
            settings.PROJECT_ROOT, settings.MEDIA_URL, self.pk))
        self.pdf_path = pth
        HTML(string=html, encoding="utf8").write_pdf(target=pth)

    def get_absolute_url(self):
        return reverse('invoice_edit', args=[str(self.id)])

    def get_document_url(self):
        return reverse('invoice_detail', args=[str(self.id)])

    def get_price(self):
        return "%s %s" % (self.cart.total_price(), self.contract.default_currency)

    def __unicode__(self):
        return _("Invoice") + " #" + str(self.id)

    @transaction.atomic()
    @reversion.create_revision()
    def save(self, *args, **kwargs):
        self.cart.last_updated = datetime.now()
        self.cart.save()
        super(Invoice, self).save(*args, **kwargs)
        self.contract.state = 30
        self.contract.save()
        self.create_pdf()


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

    class Meta:
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')
        permissions = (
            ('view_tax', 'Can view tax rates'),
        )

    def __unicode__(self):
        return self.name


class UnitTransform(models.Model):
    from_unit = models.ForeignKey(Unit, verbose_name=_("From Unit"), related_name="db_reltransformfromunit")
    to_unit = models.ForeignKey(Unit, verbose_name=_("To Unit"), related_name="db_reltransformtounit")
    product = models.ForeignKey(cartridge_models.Product, verbose_name=_("Product"))
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


class HTMLFile(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=60)
    file = FileBrowseField(verbose_name=_("HTML File"), max_length=200)

    class Meta:
        verbose_name = _('HTML File')
        verbose_name_plural = _('HTML Files')

    def __unicode__(self):
        return self.title


class TemplateSet(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=60)
    invoice_html_file = models.ForeignKey(
        HTMLFile, verbose_name=_("HTML File for Invoice"), related_name="invoice_template")
    quote_html_file = models.ForeignKey(HTMLFile, verbose_name=_("HTML File for Quote"), related_name="quote_template")
    purchaseorder_html_file = models.ForeignKey(
        HTMLFile, verbose_name=_("HTML File for Purchaseorder"), related_name="purchaseorder_template")

    class Meta:
        verbose_name = _('Templateset')
        verbose_name_plural = _('Templatesets')

    def __unicode__(self):
        return self.title


class CompanyContactData(SingletonModel):
    name = models.CharField(max_length=300, verbose_name=_("Name"))
    slogan = models.CharField(verbose_name=_("Slogan"), max_length=120, blank=True, null=True)
    logo = models.ImageField(verbose_name=_("Logo"), blank=True, null=True, max_length=200)
    addresser = models.CharField(max_length=200, verbose_name=_("Addresser"), blank=True, null=True)
    addressline1 = models.CharField(max_length=200, verbose_name=_("Addressline 1"), blank=True, null=True)
    addressline2 = models.CharField(max_length=200, verbose_name=_("Addressline 2"), blank=True, null=True)
    zipcode = models.IntegerField(verbose_name=_("Zipcode"), blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name=_("City"), blank=True, null=True)
    state = models.CharField(max_length=100, verbose_name=_("State"), blank=True, null=True)
    country = models.CharField(max_length=2, choices=countries, verbose_name=_("Country"), blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"), blank=True, null=True)
    email = models.EmailField(max_length=200, verbose_name=_("Email Address"), blank=True, null=True)
    header_text_salesorders = models.TextField(verbose_name=_("Header Text On Salesorders"), blank=True, null=True)
    header_text_purchaseorders = models.TextField(
        verbose_name=_("Header Text On Purchaseorders"), blank=True, null=True)
    page_footer_left = models.CharField(max_length=40, verbose_name=_("Page Footer Left"), blank=True, null=True)
    footer_text_salesorders = models.TextField(verbose_name=_("Footer Text On Salesorders"), blank=True, null=True)
    footer_text_purchaseorders = models.TextField(
        verbose_name=_("Footer Text On Purchaseorders"), blank=True, null=True)

    class Meta:
        verbose_name = _('Company settings')
        verbose_name_plural = _('Company settings')

    def __unicode__(self):
        return self.name


class UserExtension(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='extension', verbose_name=_('Benutzer'))
    image = models.ImageField(
        upload_to='avatars/', default='avatars/avatar.jpg', verbose_name=_('Bild'), null=True, blank=True)
    default_templateset = models.ForeignKey(TemplateSet, verbose_name=_('Vorlagen'), null=True, blank=True)
    default_currency = models.CharField(
        verbose_name=_('Currency'), max_length=3, choices=currencies, null=True, blank=True)

    class Meta:
        verbose_name = _('User Extension')
        verbose_name_plural = _('User Extensions')

    def __unicode__(self):
        return self.user.__unicode__()


class ProductUnit(models.Model):
    product = models.OneToOneField(cartridge_models.Product, verbose_name=_('Product'), related_name='item_unit')
    unit = models.ForeignKey(Unit, verbose_name=_('Unit'))

    class Meta:
        verbose_name = _('Product Unit')
        verbose_name_plural = _('Product Units')

    def __unicode__(self):
        return "%s [%s]" % (self.product, self.unit)


class ProductTax(models.Model):
    product = models.OneToOneField(cartridge_models.Product, verbose_name=_('Product'), related_name='item_tax')
    tax = models.ForeignKey(TaxRate, verbose_name=_('Tax Rate'))

    class Meta:
        verbose_name = _('Product Taxrate')
        verbose_name_plural = _('Product Taxrates')

    def __unicode__(self):
        return "%s [%s]" % (self.product, self.tax)
