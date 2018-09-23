# -*- coding: utf-8 -*-

import os
from subprocess import check_output
from subprocess import STDOUT
from django.conf import settings
from django.core import serializers
from lxml import etree
import koalixcrm.crm.documents.sales_document
import koalixcrm.djangoUserExtension.models


class PDFExport:

    @staticmethod
    def find_element_in_xml(xml_string, find_pattern, find_value):
        parser = etree.XMLParser(encoding='utf-8', remove_blank_text=True)
        root_element = etree.fromstring(xml_string.encode('utf-8'), parser=parser)
        found_element = root_element.findall(find_pattern)
        if found_element is None:
            return 0
        else:
            for element in found_element:
                if element.text == find_value:
                    return 1
            return 0

    @staticmethod
    def append_element_to_pattern(xml_string, find_pattern, name_of_element, value_of_element, **kwargs):
        attributes = kwargs.get('attributes', None)
        parser = etree.XMLParser(encoding='utf-8', remove_blank_text=True)
        root_element = etree.fromstring(xml_string.encode('utf-8'), parser=parser)
        found_element = root_element.find(find_pattern)
        new_element = etree.SubElement(found_element, name_of_element, attrib=attributes)
        new_element.text = value_of_element.__str__()
        return (etree.tostring(root_element,
                               encoding='UTF-8',
                               xml_declaration=True,
                               pretty_print=True)).decode('utf-8')

    @staticmethod
    def merge_xml(xml_string_1, xml_string_2):
        parser = etree.XMLParser(encoding='utf-8', remove_blank_text=True)
        root_element_1 = etree.fromstring(xml_string_1.encode('utf-8'), parser=parser)
        root_element_2 = etree.fromstring(xml_string_2.encode('utf-8'), parser=parser)
        for child in root_element_2:
            root_element_1.append(child)
        return (etree.tostring(root_element_1,
                               encoding='UTF-8',
                               xml_declaration=True,
                               pretty_print=True)).decode('utf-8')

    @staticmethod
    def write_xml(objects_to_serialize):
        xml = serializers.serialize("xml", objects_to_serialize, indent=3)
        return xml

    @staticmethod
    def write_xml_file(xml, file_path):
        f = open(file_path, "wb+")
        f.truncate()
        f.write(xml.encode('utf-8'))
        f.close()

    @staticmethod
    def perform_xsl_transformation(file_with_serialized_xml, xsl_file, fop_config_file, file_output_pdf):
        check_output([settings.FOP_EXECUTABLE,
                      '-c', fop_config_file.path_full,
                      '-xml', os.path.join(settings.PDF_OUTPUT_ROOT, file_with_serialized_xml),
                      '-xsl', xsl_file.path_full,
                      '-pdf', file_output_pdf], stderr=STDOUT)

    @staticmethod
    def create_pdf(object_to_create_pdf, template_set, printed_by, *args, **kwargs):
        # define the files which are involved in pdf creation process
        fop_config_file = object_to_create_pdf.get_fop_config_file(template_set)
        xsl_file = object_to_create_pdf.get_xsl_file(template_set)
        file_with_serialized_xml = os.path.join(settings.PDF_OUTPUT_ROOT, (str(type(object_to_create_pdf).__name__) +
                                                                           "_" + str(object_to_create_pdf.id) + ".xml"))
        file_output_pdf = os.path.join(settings.PDF_OUTPUT_ROOT, (str(type(object_to_create_pdf).__name__) +
                                                                  "_" + str(object_to_create_pdf.id) + ".pdf"))

        # list the sub-objects which have to be serialized
        xml_string = object_to_create_pdf.serialize_to_xml(*args, **kwargs)
        objects_to_serialize = list(koalixcrm.djangoUserExtension.models.DocumentTemplate.objects.filter(id=template_set.id))
        xml_string_temp = PDFExport.write_xml(objects_to_serialize)
        xml_string = PDFExport.merge_xml(xml_string, xml_string_temp)
        objects_to_serialize = koalixcrm.djangoUserExtension.models.UserExtension.objects_to_serialize(object_to_create_pdf, printed_by)
        xml_string_temp = PDFExport.write_xml(objects_to_serialize)
        xml_string = PDFExport.merge_xml(xml_string, xml_string_temp)

        # extend the xml-string with required basic settings
        xml_string = PDFExport.append_element_to_pattern(xml_string,
                                                         ".",
                                                         "filebrowser_directory",
                                                         settings.MEDIA_ROOT)

        #  write xml-string to xml-file
        PDFExport.write_xml_file(xml_string, file_with_serialized_xml)

        # perform xsl transformation
        PDFExport.perform_xsl_transformation(file_with_serialized_xml, xsl_file, fop_config_file, file_output_pdf)

        return file_output_pdf
