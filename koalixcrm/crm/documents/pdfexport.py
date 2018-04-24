# -*- coding: utf-8 -*-

import os
from subprocess import check_output
from subprocess import STDOUT
from django.conf import settings
from django.core import serializers
from django.utils.translation import ugettext as _
from koalixcrm.crm.exceptions import *
from koalixcrm import djangoUserExtension
from koalixcrm.crm.contact.contact import Contact
from lxml import etree
from koalixcrm.crm.documents.salesdocumentposition import Position
import koalixcrm.crm.documents.salesdocument
import koalixcrm.accounting


class PDFExport:

    @staticmethod
    def extend_xml_with_root_element(file_with_serialized_xml):
        xml = etree.parse(file_with_serialized_xml)
        root_element = xml.getroot()
        filebrowser_directory = etree.SubElement(root_element, "filebrowser_directory")
        filebrowser_directory.text = settings.MEDIA_ROOT
        xml.write(file_with_serialized_xml)

    @staticmethod
    def add_accounts(objects_to_serialize, object_to_create_pdf):
        objects_to_serialize += list(koalixcrm.accounting.models.Acount.all())
        return objects_to_serialize

    @staticmethod
    def create_list_of_objects_to_serialize(object_to_create_pdf):
        if isinstance(object_to_create_pdf, koalixcrm.crm.documents.salesdocument.SalesDocument):
            return koalixcrm.crm.documents.salesdocument.SalesDocument.objects_to_serialize(object_to_create_pdf)
        elif isinstance(object_to_create_pdf, koalixcrm.accounting.models.AccoutingPeriod):
            return PDFExport.create_list_of_objects_to_serialize_accounting_period(object_to_create_pdf)
        else:
            raise NoSerializationPatternFound(_("During "+str(object_to_create_pdf)+" PDF Export"))

    @staticmethod
    def create_list_of_objects_to_serialize_accounting_period(object_to_create_pdf):
        objects_to_serialize = list(type(object_to_create_pdf).objects.filter(id=object_to_create_pdf.id))
        objects_to_serialize += koalixcrm.djangoUserExtension.models.UserExtension.objects_to_serialize(object_to_create_pdf)
        objects_to_serialize += PDFExport.add_accounts(objects_to_serialize, object_to_create_pdf)
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
    def create_pdf(object_to_create_pdf, template_set):
        # define the files which are involved in pdf creation process
        fop_config_file = object_to_create_pdf.get_fop_config_file(template_set)
        xsl_file = object_to_create_pdf.get_xsl_file(template_set)
        file_with_serialized_xml = os.path.join(settings.PDF_OUTPUT_ROOT, (str(type(object_to_create_pdf).__name__) +
                                                                           "_" + str(object_to_create_pdf.id) + ".xml"))
        file_output_pdf = os.path.join(settings.PDF_OUTPUT_ROOT, (str(type(object_to_create_pdf).__name__) +
                                                                  "_" + str(object_to_create_pdf.id) + ".pdf"))

        # list the sub-objects which to be serialized
        objects_to_serialize = PDFExport.create_list_of_objects_to_serialize(object_to_create_pdf)

        # serialize the objects to xml-file
        PDFExport.write_xml_file(objects_to_serialize, file_with_serialized_xml)

        # extend the xml-file with required basic settings
        PDFExport.extend_xml_with_root_element(file_with_serialized_xml)

        # perform xsl transformation
        PDFExport.perform_xsl_transformation(file_with_serialized_xml, xsl_file, fop_config_file, file_output_pdf)

        return file_output_pdf
