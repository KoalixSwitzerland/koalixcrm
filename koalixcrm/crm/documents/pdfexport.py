# -*- coding: utf-8 -*-

import os
from subprocess import check_output
from subprocess import STDOUT

from django.conf import settings
from django.contrib import auth
from django.core import serializers
from django.utils.translation import ugettext as _
from koalixcrm.crm.exceptions import *
from koalixcrm import djangoUserExtension
from koalixcrm.crm.contact.contact import Contact
from koalixcrm.crm.contact.contact import PostalAddressForContact
from koalixcrm.crm.contact.phoneaddress import PhoneAddress
from koalixcrm.crm.contact.emailaddress import EmailAddress
from koalixcrm.crm.contact.postaladdress import PostalAddress
from koalixcrm.crm.product.currency import Currency
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.product.product import Product
from lxml import etree

from koalixcrm.crm.documents.salesdocumentposition import Position
import koalixcrm.crm.documents.purchaseorder
import koalixcrm.crm.documents.salesdocument


class PDFExport:

    @staticmethod
    def extend_xml_with_root_element(file_with_serialized_xml):
        xml = etree.parse(file_with_serialized_xml)
        root_element = xml.getroot()
        filebrowser_directory = etree.SubElement(root_element, "filebrowser_directory")
        filebrowser_directory.text = settings.MEDIA_ROOT
        xml.write(file_with_serialized_xml)

    @staticmethod
    def add_positions(objects_to_serialize, position_class, object_to_create_pdf):
        objects_to_serialize += list(position_class.objects.filter(sales_document=object_to_create_pdf.id))
        for position in list(position_class.objects.filter(sales_document=object_to_create_pdf.id)):
            objects_to_serialize += list(Position.objects.filter(id=position.id))
            objects_to_serialize += list(Product.objects.filter(id=position.product.id))
            objects_to_serialize += list(Unit.objects.filter(id=position.unit.id))
        return objects_to_serialize

    @staticmethod
    def create_list_of_objects_to_serialize(object_to_create_pdf):

        # define options for the serialization (options depend on which main object need to be serialized)
        if isinstance(object_to_create_pdf, koalixcrm.crm.documents.salesdocument.SalesDocument):
            position_class = koalixcrm.crm.documents.salesdocumentposition.SalesDocumentPosition
            export_customer = True
            export_supplier = False
        else:
            position_class = koalixcrm.crm.documents.purchaseorder.PurchaseOrderPosition
            export_customer = False
            export_supplier = True

        objects_to_serialize = list(type(object_to_create_pdf).objects.filter(id=object_to_create_pdf.id))
        if export_supplier:
            objects_to_serialize += list(Contact.objects.filter(id=object_to_create_pdf.supplier.id))
            objects_to_serialize += list(PostalAddressForContact.objects.filter(person=object_to_create_pdf.supplier.id))
            for address in list(PostalAddressForContact.objects.filter(person=object_to_create_pdf.supplier.id)):
                objects_to_serialize += list(PostalAddress.objects.filter(id=address.id))
        if export_customer:
            objects_to_serialize += list(koalixcrm.crm.documents.salesdocument.SalesDocument.objects.filter(id=object_to_create_pdf.id))
            objects_to_serialize += list(Contact.objects.filter(id=object_to_create_pdf.customer.id))
            objects_to_serialize += list(PostalAddressForContact.objects.filter(person=object_to_create_pdf.customer.id))
            for address in list(PostalAddressForContact.objects.filter(person=object_to_create_pdf.customer.id)):
                objects_to_serialize += list(PostalAddress.objects.filter(id=address.id))
            objects_to_serialize += list(koalixcrm.crm.documents.salesdocument.TextParagraphInSalesDocument.objects.filter(sales_document=object_to_create_pdf.id))
        objects_to_serialize += list(Currency.objects.filter(id=object_to_create_pdf.currency.id))
        objects_to_serialize = PDFExport.add_positions(objects_to_serialize, position_class, object_to_create_pdf)
        objects_to_serialize += list(auth.models.User.objects.filter(id=object_to_create_pdf.staff.id))
        userExtension = djangoUserExtension.models.UserExtension.objects.filter(user=object_to_create_pdf.staff.id)
        if len(userExtension) == 0:
            raise UserExtensionMissing(_("During "+str(object_to_create_pdf)+" PDF Export"))
        phone_address = djangoUserExtension.models.UserExtensionPhoneAddress.objects.filter(
            userExtension=userExtension[0].id)
        if len(phone_address) == 0:
            raise UserExtensionPhoneAddressMissing(_("During "+type(object_to_create_pdf)+" PDF Export"))
        email_address = djangoUserExtension.models.UserExtensionEmailAddress.objects.filter(
            userExtension=userExtension[0].id)
        if len(email_address) == 0:
            raise UserExtensionEmailAddressMissing(_("During "+type(object_to_create_pdf)+" PDF Export"))
        objects_to_serialize += list(userExtension)
        objects_to_serialize += list(EmailAddress.objects.filter(id=email_address[0].id))
        objects_to_serialize += list(PhoneAddress.objects.filter(id=phone_address[0].id))
        template_set = djangoUserExtension.models.DocumentTemplate.objects.filter(
            id=object_to_create_pdf.template_set.id)
        if len(template_set) == 0:
            raise TemplateSetMissing(_("During "+type(object_to_create_pdf)+" PDF Export"))
        objects_to_serialize += list(template_set)
        return objects_to_serialize

    @staticmethod
    def write_xml_file(objects_to_serialize, file_with_serialized_xml):
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        out = open(file_with_serialized_xml, "wb")
        xml_serializer.serialize(objects_to_serialize, stream=out, indent=3)
        out.close()

    @staticmethod
    def perform_xsl_transformation(file_with_serialized_xml, xsl_file, fop_config_file, file_output_pdf):
        check_output([settings.FOP_EXECUTABLE,
                      '-c', fop_config_file.path_full,
                      '-xml', os.path.join(settings.PDF_OUTPUT_ROOT, file_with_serialized_xml),
                      '-xsl', xsl_file.path_full,
                      '-pdf', file_output_pdf], stderr=STDOUT)

    @staticmethod
    def create_pdf(object_to_create_pdf):
        # define the files which are involved in pdf creation process
        fop_config_file = object_to_create_pdf.get_fop_config_file()
        xsl_file = object_to_create_pdf.get_xsl_file()
        file_with_serialized_xml = os.path.join(settings.PDF_OUTPUT_ROOT, (str(object_to_create_pdf) + ".xml"))
        file_output_pdf = os.path.join(settings.PDF_OUTPUT_ROOT, (str(object_to_create_pdf) + ".pdf"))

        # list the sub-objects which to be serialized
        objects_to_serialize = PDFExport.create_list_of_objects_to_serialize(object_to_create_pdf)

        # serialize the objects to xml-file
        PDFExport.write_xml_file(objects_to_serialize, file_with_serialized_xml)

        # extend the xml-file with required basic settings
        PDFExport.extend_xml_with_root_element(file_with_serialized_xml)

        # perform xsl transformation
        PDFExport.perform_xsl_transformation(file_with_serialized_xml, xsl_file, fop_config_file, file_output_pdf)

        return file_output_pdf
