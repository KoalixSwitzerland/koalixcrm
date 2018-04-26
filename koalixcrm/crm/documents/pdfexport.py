# -*- coding: utf-8 -*-

import os
from subprocess import check_output
from subprocess import STDOUT
from django.conf import settings
from django.core import serializers
from django.utils.translation import ugettext as _
from koalixcrm.crm.exceptions import *
from koalixcrm.crm.contact.contact import Contact
from lxml import etree
from koalixcrm.crm.documents.salesdocumentposition import Position
import koalixcrm.crm.documents.salesdocument
import koalixcrm.accounting.models
import koalixcrm.djangoUserExtension.models


class PDFExport:

    @staticmethod
    def extend_xml_with_root_element(xml_string):
        parser = etree.XMLParser(encoding='utf-8')
        root_element = etree.fromstring(xml_string.encode('utf-8'), parser=parser)
        filebrowser_directory = etree.SubElement(root_element, "filebrowser_directory")
        filebrowser_directory.text = settings.MEDIA_ROOT
        return (etree.tostring(root_element, encoding='UTF-8', xml_declaration=True)).decode('utf-8')

    @staticmethod
    def merge_xml(xml_string_1, xml_string_2):
        parser = etree.XMLParser(encoding='utf-8')
        root_element_1 = etree.fromstring(xml_string_1.encode('utf-8'), parser=parser)
        root_element_2 = etree.fromstring(xml_string_2.encode('utf-8'), parser=parser)
        for child in root_element_2:
            root_element_1.append(child)
        return (etree.tostring(root_element_1, encoding='UTF-8', xml_declaration=True)).decode('utf-8')


    @staticmethod
    def create_list_of_objects_to_serialize(object_to_create_pdf):
        if isinstance(object_to_create_pdf, koalixcrm.crm.documents.salesdocument.SalesDocument):
            return koalixcrm.crm.documents.salesdocument.SalesDocument.objects_to_serialize(object_to_create_pdf)
        elif isinstance(object_to_create_pdf, koalixcrm.accounting.models.AccountingPeriod):
            return koalixcrm.accounting.models.AccountingPeriod.objects_to_serialize(object_to_create_pdf)
        else:
            raise NoSerializationPatternFound(_("During "+str(object_to_create_pdf)+" PDF Export"))

    @staticmethod
    def write_xml(objects_to_serialize):
        xml = serializers.serialize("xml", objects_to_serialize, indent=3)
        return xml

    @staticmethod
    def write_xml_file(xml, file_path):
        xml.encode('utf-8')
        f = open(file_path, "w+")
        f.truncate()
        f.write(xml)
        f.close()


    @staticmethod
    def perform_xsl_transformation(file_with_serialized_xml, xsl_file, fop_config_file, file_output_pdf):
        check_output([settings.FOP_EXECUTABLE,
                      '-c', fop_config_file.path_full,
                      '-xml', os.path.join(settings.PDF_OUTPUT_ROOT, file_with_serialized_xml),
                      '-xsl', xsl_file.path_full,
                      '-pdf', file_output_pdf], stderr=STDOUT)

    @staticmethod
    def create_pdf(object_to_create_pdf, template_set, printed_by):
        # define the files which are involved in pdf creation process
        fop_config_file = object_to_create_pdf.get_fop_config_file(template_set)
        xsl_file = object_to_create_pdf.get_xsl_file(template_set)
        file_with_serialized_xml = os.path.join(settings.PDF_OUTPUT_ROOT, (str(type(object_to_create_pdf).__name__) +
                                                                           "_" + str(object_to_create_pdf.id) + ".xml"))
        file_output_pdf = os.path.join(settings.PDF_OUTPUT_ROOT, (str(type(object_to_create_pdf).__name__) +
                                                                  "_" + str(object_to_create_pdf.id) + ".pdf"))

        # list the sub-objects which have to be serialized
        objects_to_serialize = PDFExport.create_list_of_objects_to_serialize(object_to_create_pdf)
        xml_string_1 = PDFExport.write_xml(objects_to_serialize)
        objects_to_serialize = list(koalixcrm.djangoUserExtension.models.DocumentTemplate.objects.filter(id=template_set.id))
        xml_string_2 = PDFExport.write_xml(objects_to_serialize)
        objects_to_serialize = koalixcrm.djangoUserExtension.models.UserExtension.objects_to_serialize(object_to_create_pdf, printed_by)
        xml_string_3 = PDFExport.write_xml(objects_to_serialize)

        xml_string = PDFExport.merge_xml(xml_string_1, xml_string_2)
        xml_string = PDFExport.merge_xml(xml_string, xml_string_3)

        # extend the xml-string with required basic settings
        xml_string = PDFExport.extend_xml_with_root_element(xml_string)

        #  write xml-string to xml-file
        PDFExport.write_xml_file(xml_string, file_with_serialized_xml)

        # perform xsl transformation
        PDFExport.perform_xsl_transformation(file_with_serialized_xml, xsl_file, fop_config_file, file_output_pdf)


        return file_output_pdf
