# -*- coding: utf-8 -*-

from datetime import *
from django.db import models
from django.contrib import admin, messages
from django.utils.translation import gettext as _
from koalixcrm.core.const.purpose import *
from koalixcrm.global_support_functions import xstr, make_date_utc
from koalixcrm.contacts.models.phone_address import PhoneAddress
from koalixcrm.contacts.models.email_address import EmailAddress
from koalixcrm.contacts.models.postal_address import PostalAddress
from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition
from koalixcrm.djangoUserExtension.models import TextParagraphInDocumentTemplate, UserExtension
from koalixcrm.products.models.product_type import ProductType
from koalixcrm.core.exceptions import TemplateSetMissingInContract
import koalixcrm.contracts.models.calculations
from koalixcrm.shared.pdf_export import PDFExport


class TextParagraphInCommercialDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    commercial_document = models.ForeignKey("CommercialDocument", on_delete=models.CASCADE)
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=2, choices=PURPOSESTEXTPARAGRAPHINDOCUMENTS)
    text_paragraph = models.TextField(verbose_name=_("Text"), blank=False, null=False)

    def create_paragraph(self, default_paragraph, commercial_document):
        self.commercial_document = commercial_document
        self.purpose = default_paragraph.purpose
        self.text_paragraph = default_paragraph.text_paragraph
        self.save()
        return

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_textparagraphincommercialdocument"
        verbose_name = _('Text Paragraph In Commercial Document')
        verbose_name_plural = _('Text Paragraphs In Commercial Documents')

    def __str__(self):
        return self.id.__str__()


class CommercialDocument(models.Model):
    contract = models.ForeignKey("Contract",
                                 on_delete=models.CASCADE,
                                 verbose_name=_('Contract'))
    external_reference = models.CharField(verbose_name=_("External Reference"),
                                          max_length=100,
                                          blank=True)
    discount = models.DecimalField(max_digits=5,
                                   decimal_places=2,
                                   verbose_name=_("Discount"),
                                   blank=True,
                                   null=True)
    description = models.CharField(verbose_name=_("Description"),
                                   max_length=100,
                                   blank=True,
                                   null=True)
    last_pricing_date = models.DateField(verbose_name=_("Pricing Date"),
                                         blank=True,
                                         null=True)
    last_calculated_price = models.DecimalField(max_digits=17,
                                                decimal_places=2,
                                                verbose_name=_("Price without Tax "),
                                                blank=True,
                                                null=True)
    last_calculated_tax = models.DecimalField(max_digits=17,
                                              decimal_places=2,
                                              verbose_name=_("Tax"),
                                              blank=True,
                                              null=True)
    customer = models.ForeignKey("contacts.Customer",
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Customer"))
    staff = models.ForeignKey('auth.User',
                              on_delete=models.CASCADE,
                              limit_choices_to={'is_staff': True},
                              blank=True,
                              verbose_name=_("Staff"),
                              related_name="db_relscstaff",
                              null=True)
    currency = models.ForeignKey("core.Currency", on_delete=models.CASCADE, verbose_name=_("Currency"),
                                 blank=False, null=False)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)
    custom_date_field = models.DateField(verbose_name=_("Custom Date"),
                                         blank=True,
                                         null=True)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         related_name="db_lstscmodified",
                                         null=True,
                                         blank="True")
    template_set = models.ForeignKey("djangoUserExtension.DocumentTemplate",
                                     on_delete=models.CASCADE,
                                     verbose_name=_("Referred Template"),
                                     null=True,
                                     blank=True)
    derived_from_commercial_document = models.ForeignKey("CommercialDocument",
                                                    on_delete=models.CASCADE,
                                                    blank=True,
                                                    null=True)
    last_print_date = models.DateTimeField(verbose_name=_("Last printed"),
                                           blank=True,
                                           null=True)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_commercialdocument"
        verbose_name = _('Commercial Document')
        verbose_name_plural = _('Commercial Documents')

    def serialize_to_xml(self):
        from koalixcrm.contacts.models import PostalAddressForContact
        from koalixcrm.contacts.models import Contact
        from koalixcrm.core.models import Currency
        from koalixcrm.contracts.models.purchase_order import PurchaseOrder
        from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition
        from django.contrib import auth
        objects = [self, ]
        position_class = CommercialDocumentPosition
        objects += list(CommercialDocument.objects.filter(id=self.id))
        if isinstance(self, PurchaseOrder):
            objects += list(Contact.objects.filter(id=self.supplier.id))
            objects += list(PostalAddressForContact.objects.filter(person=self.supplier.id))
            for address in list(PostalAddressForContact.objects.filter(person=self.supplier.id)):
                objects += list(PostalAddress.objects.filter(id=address.id))
        else:
            objects += list(Contact.objects.filter(id=self.customer.id))
            objects += list(PostalAddressForContact.objects.filter(person=self.customer.id))
            for address in list(PostalAddressForContact.objects.filter(person=self.customer.id)):
                objects += list(PostalAddress.objects.filter(id=address.id))
        objects += list(TextParagraphInCommercialDocument.objects.filter(commercial_document=self.id))
        objects += list(Currency.objects.filter(id=self.currency.id))
        objects += CommercialDocumentPosition.add_positions(position_class, self)
        objects += list(auth.models.User.objects.filter(id=self.staff.id))
        objects += UserExtension.objects_to_serialize(self, self.staff)
        main_xml = PDFExport.write_xml(objects)
        return main_xml

    def is_complete_with_price(self):
        """ Checks whether the CommercialDocument is completed with a price, in case the
        CommercialDocument was not completed or the price calculation was not performed,
        the method returns false"""

        if self.last_pricing_date and self.last_calculated_price:
            return True
        else:
            return False

    def create_commercial_document(self, calling_model):
        self.staff = calling_model.staff
        if isinstance(calling_model, koalixcrm.contracts.models.contract.Contract):
            self.contract = calling_model
            self.customer = calling_model.default_customer
            self.currency = calling_model.default_currency
            self.description = calling_model.description
            self.discount = 0
        elif isinstance(calling_model, CommercialDocument):
            self.derived_from_commercial_document = calling_model
            self.contract = calling_model.contract
            self.customer = calling_model.customer
            self.currency = calling_model.currency
            self.description = calling_model.description
            self.discount = calling_model.discount

    def attach_text_paragraphs(self):
        default_paragraphs = TextParagraphInDocumentTemplate.objects.filter(document_template=self.template_set)
        for default_paragraph in list(default_paragraphs):
            paragraph = TextParagraphInCommercialDocument()
            paragraph.create_paragraph(default_paragraph, self)

    def attach_commercial_document_positions(self, calling_model):
        if isinstance(calling_model, CommercialDocument):
            commercial_document_positions = CommercialDocumentPosition.objects.filter(commercial_document=calling_model.id)
            for commercial_document_position in list(commercial_document_positions):
                new_position = CommercialDocumentPosition()
                new_position.create_position(commercial_document_position, self)

    def create_pdf(self, template_set, printed_by):
        self.last_print_date = make_date_utc(datetime.now())
        self.save()
        return koalixcrm.core.documents.pdf_export.PDFExport.create_pdf(self, template_set, printed_by)

    def get_template_set(self):
        if self.template_set:
            return self.template_set
        else:
            raise TemplateSetMissingInContract((_("Template Set missing in Commercial Document" + str(self))))

    def get_fop_config_file(self, template_set):
        template_set = self.get_template_set()
        return template_set.get_fop_config_file()

    def get_xsl_file(self, template_set):
        template_set = self.get_template_set()
        return template_set.get_xsl_file()

    def __str__(self):
        return _("Commercial Document") + ": " + str(self.id) + " " + _("from Contract") + ": " + str(self.contract.id)


class PostalAddressForCommercialDocument(PostalAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    commercial_document = models.ForeignKey("CommercialDocument", on_delete=models.CASCADE)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_postaladdressforcommercialdocument"
        verbose_name = _('Postal Address For Commercial Documents')
        verbose_name_plural = _('Postal Address For Commercial Documents')

    def __str__(self):
        return xstr(self.pre_name) + ' ' + xstr(self.name) + ' ' + xstr(self.address_line_1)


class EmailAddressForCommercialDocument(EmailAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    commercial_document = models.ForeignKey("CommercialDocument", on_delete=models.CASCADE)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_emailaddressforcommercialdocument"
        verbose_name = _('Email Address For Commercial Documents')
        verbose_name_plural = _('Email Address For Commercial Documents')

    def __str__(self):
        return str(self.email)


class PhoneAddressForCommercialDocument(PhoneAddress):
    purpose = models.CharField(verbose_name=_("Purpose"), max_length=1, choices=PURPOSESADDRESSINCONTRACT)
    commercial_document = models.ForeignKey("CommercialDocument", on_delete=models.CASCADE)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_phoneaddressforcommercialdocument"
        verbose_name = _('Phone Address For Commercial Documents')
        verbose_name_plural = _('Phone Address For Commercial Documents')

    def __str__(self):
        return str(self.phone)
