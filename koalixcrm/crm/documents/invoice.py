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
from koalixcrm.crm.exceptions import *
from koalixcrm import accounting
from koalixcrm import djangoUserExtension
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


class Invoice(SalesContract):
    payableuntil = models.DateField(verbose_name=_("To pay until"))
    derivatedFromQuote = models.ForeignKey("Quote", blank=True, null=True)
    paymentBankReference = models.CharField(verbose_name=_("Payment Bank Reference"), max_length=100, blank=True,
                                            null=True)
    status = models.CharField(max_length=1, choices=INVOICESTATUS)

    def isComplete(self):
        """ Checks whether the Invoice is completed with a price, in case the invoice
        was not completed or the price calculation was not performed, the method
        returns false"""

        if self.lastPricingDate and self.lastCalculatedPrice:
            return True
        else:
            return False

    def registerinvoiceinaccounting(self, request):
        dictprices = dict()
        dicttax = dict()
        currentValidAccountingPeriod = accounting.models.AccountingPeriod.getCurrentValidAccountingPeriod()
        activaaccount = accounting.models.Account.objects.filter(isopeninterestaccount=True)
        if not self.isComplete():
            raise IncompleteInvoice(_("Complete invoice and run price recalculation. Price may not be Zero"))
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

    def createPDF(self):
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        self.last_print_date = datetime.now()
        self.save()
        out = open(os.path.join(settings.PDF_OUTPUT_ROOT, "invoice_" + str(self.id) + ".xml"), "wb")
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
        userExtension = djangoUserExtension.models.UserExtension.objects.filter(user=self.staff.id)
        if (len(userExtension) == 0):
            raise UserExtensionMissing(_("During Invoice PDF Export"))
        phoneAddress = djangoUserExtension.models.UserExtensionPhoneAddress.objects.filter(
            userExtension=userExtension[0].id)
        if len(phoneAddress) == 0:
            raise UserExtensionPhoneAddressMissing(_("During Quote PDF Export"))
        email_address = djangoUserExtension.models.UserExtensionEmailAddress.objects.filter(
            userExtension=userExtension[0].id)
        if len(email_address) == 0:
            raise UserExtensionEmailAddressMissing(_("During Quote PDF Export"))
        objects_to_serialize += list(userExtension)
        objects_to_serialize += list(PhoneAddress.objects.filter(id=phoneAddress[0].id))
        objects_to_serialize += list(EmailAddress.objects.filter(id=email_address[0].id))
        templateset = djangoUserExtension.models.TemplateSet.objects.filter(id=userExtension[0].defaultTemplateSet.id)
        if (len(templateset) == 0):
            raise TemplateSetMissing(_("During Invoice PDF Export"))
        objects_to_serialize += list(templateset)
        objects_to_serialize += list(auth.models.User.objects.filter(id=self.lastmodifiedby.id))
        objects_to_serialize += list(PostalAddressForContact.objects.filter(person=self.customer.id))
        for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
            objects_to_serialize += list(PostalAddress.objects.filter(id=address.id))
        xml_serializer.serialize(objects_to_serialize, stream=out, indent=3)
        out.close()
        xml = etree.parse(os.path.join(settings.PDF_OUTPUT_ROOT, ("invoice_" + str(self.id) + ".xml")))
        rootelement = xml.getroot()
        filebrowserdirectory = etree.SubElement(rootelement, "filebrowserdirectory")
        filebrowserdirectory.text = settings.MEDIA_ROOT
        xml.write(os.path.join(settings.PDF_OUTPUT_ROOT, ("invoice_" + str(self.id) + ".xml")))
        check_output(
            [settings.FOP_EXECUTABLE, '-c', userExtension[0].defaultTemplateSet.fopConfigurationFile.path_full, '-xml',
             os.path.join(settings.PDF_OUTPUT_ROOT, ('invoice_' + str(self.id) + '.xml')), '-xsl',
             userExtension[0].defaultTemplateSet.invoiceXSLFile.xslfile.path_full, '-pdf',
             os.path.join(settings.PDF_OUTPUT_ROOT, ('invoice_' + str(self.id) + '.pdf'))], stderr=STDOUT)
        return os.path.join(settings.PDF_OUTPUT_ROOT, ("invoice_" + str(self.id) + ".pdf"))
        #  TODO: def registerPayment(self, amount, registerpaymentinaccounting):

    def __str__(self):
        return _("Invoice") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')