import os
from datetime import *
from subprocess import check_output
from subprocess import STDOUT

from django.conf import settings
from django.contrib import auth
from django.core import serializers
from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.const.status import *
from koalixcrm import djangoUserExtension
from koalixcrm.crm.exceptions import *
from koalixcrm.crm.documents.invoice import Invoice
from koalixcrm.crm.contact.contact import Contact
from koalixcrm.crm.contact.contact import PostalAddressForContact
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.product.currency import Currency
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.product.product import Product
from koalixcrm.crm.documents.salescontract import SalesContract
from koalixcrm.crm.documents.salescontractposition import SalesContractPosition
from koalixcrm.crm.documents.salescontractposition import Position
from lxml import etree

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

    def createPDF(self):
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        self.last_print_date = datetime.now()
        self.save()
        out = open(os.path.join(settings.PDF_OUTPUT_ROOT, ("quote_" + str(self.id) + ".xml")), "wb")
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
        userExtension = djangoUserExtension.models.UserExtension.objects.filter(user=self.staff.id)
        if (len(userExtension) == 0):
            raise UserExtensionMissing(_("During Quote PDF Export"))
        phoneAddress = djangoUserExtension.models.UserExtensionPhoneAddress.objects.filter(
            userExtension=userExtension[0].id)
        if len(phoneAddress) == 0:
            raise UserExtensionPhoneAddressMissing(_("During Quote PDF Export"))
        email_address = djangoUserExtension.models.UserExtensionEmailAddress.objects.filter(
            userExtension=userExtension[0].id)
        if len(email_address) == 0:
            raise UserExtensionEmailAddressMissing(_("During Quote PDF Export"))
        objects_to_serialize += list(userExtension)
        objects_to_serialize += list(EmailAddress.objects.filter(id=email_address[0].id))
        objects_to_serialize += list(PhoneAddress.objects.filter(id=phoneAddress[0].id))
        template_set = djangoUserExtension.models.TemplateSet.objects.filter(id=self.template_set.id)
        if len(template_set) == 0:
            raise TemplateSetMissing(_("During Quote PDF Export"))
        objects_to_serialize += list(template_set)
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objects_to_serialize += list(PostalAddressForContact.objects.filter(person=self.customer.id))
        for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
            objects_to_serialize += list(PostalAddress.objects.filter(id=address.id))
        xml_serializer.serialize(objects_to_serialize, stream=out, indent=3)
        out.close()
        xml = etree.parse(os.path.join(settings.PDF_OUTPUT_ROOT, ("quote_" + str(self.id) + ".xml")))
        rootelement = xml.getroot()
        filebrowserdirectory = etree.SubElement(rootelement, "filebrowserdirectory")
        filebrowserdirectory.text = settings.MEDIA_ROOT
        xml.write(os.path.join(settings.PDF_OUTPUT_ROOT , ("quote_" + str(self.id) + ".xml")))
        check_output(
            [settings.FOP_EXECUTABLE, '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path_full, '-xml',
             os.path.join(settings.PDF_OUTPUT_ROOT, ('quote_' + str(self.id) + '.xml')), '-xsl',
             userExtension[0].defaultTemplateSet.quoteXSLFile.xslfile.path_full, '-pdf',
             os.path.join(settings.PDF_OUTPUT_ROOT, ('quote_' + str(self.id) + '.pdf'))], stderr=STDOUT)
        return os.path.join(settings.PDF_OUTPUT_ROOT, ("quote_" + str(self.id) + ".pdf"))

    def __str__(self):
        return _("Quote") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Quote')
        verbose_name_plural = _('Quotes')
