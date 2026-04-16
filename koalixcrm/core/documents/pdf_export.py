# -*- coding: utf-8 -*-

import logging
import os
import tempfile
from subprocess import check_output, CalledProcessError
from subprocess import STDOUT
from django.conf import settings
from django.core import serializers
from lxml import etree
import koalixcrm.djangoUserExtension.models

logger = logging.getLogger(__name__)


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
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        f = open(file_path, "wb+")
        f.truncate()
        f.write(xml.encode('utf-8'))
        f.close()

    @staticmethod
    def _download_s3_field_to_temp(file_field, tmp_dir, prefix=""):
        """Download an S3-backed FileField to a local temp file and return the path."""
        name = os.path.basename(file_field.name)
        local_path = os.path.join(tmp_dir, prefix + name)
        file_field.open('rb')
        try:
            with open(local_path, 'wb') as f:
                for chunk in file_field.chunks():
                    f.write(chunk)
        finally:
            file_field.close()
        return local_path

    @staticmethod
    def perform_xsl_transformation(xml_file_path, xsl_local_path, fop_config_local_path, file_output_pdf):
        cmd = [settings.FOP_EXECUTABLE,
               '-c', fop_config_local_path,
               '-xml', xml_file_path,
               '-xsl', xsl_local_path,
               '-pdf', file_output_pdf]
        try:
            check_output(cmd, stderr=STDOUT)
        except CalledProcessError as e:
            fop_output = e.output.decode('utf-8', errors='replace') if e.output else '(no output)'
            raise RuntimeError(
                f"FOP failed (exit {e.returncode}):\n{fop_output}"
            ) from e

    @staticmethod
    def create_pdf(object_to_create_pdf, template_set, printed_by, *args, **kwargs):
        # Get S3-backed template file fields
        fop_config_field = object_to_create_pdf.get_fop_config_file(template_set)
        xsl_field = object_to_create_pdf.get_xsl_file(template_set)

        # Output paths
        file_with_serialized_xml = os.path.join(
            settings.PDF_OUTPUT_ROOT,
            str(type(object_to_create_pdf).__name__) + "_" + str(object_to_create_pdf.id) + ".xml"
        )
        file_output_pdf = os.path.join(
            settings.PDF_OUTPUT_ROOT,
            str(type(object_to_create_pdf).__name__) + "_" + str(object_to_create_pdf.id) + ".pdf"
        )

        # Serialize document to XML
        xml_string = object_to_create_pdf.serialize_to_xml(*args, **kwargs)
        objects_to_serialize = list(koalixcrm.djangoUserExtension.models.DocumentTemplate.objects.filter(id=template_set.id))
        xml_string_temp = PDFExport.write_xml(objects_to_serialize)
        xml_string = PDFExport.merge_xml(xml_string, xml_string_temp)
        objects_to_serialize = koalixcrm.djangoUserExtension.models.UserExtension.objects_to_serialize(object_to_create_pdf, printed_by)
        xml_string_temp = PDFExport.write_xml(objects_to_serialize)
        xml_string = PDFExport.merge_xml(xml_string, xml_string_temp)

        xml_string = PDFExport.append_element_to_pattern(xml_string,
                                                         ".",
                                                         "filebrowser_directory",
                                                         settings.MEDIA_ROOT)

        PDFExport.write_xml_file(xml_string, file_with_serialized_xml)

        # Download S3 template files to temp dir, run FOP, then clean up
        with tempfile.TemporaryDirectory(prefix="koalixcrm_fop_") as tmp_dir:
            xsl_local = PDFExport._download_s3_field_to_temp(xsl_field, tmp_dir, prefix="xsl_")
            fop_config_local = PDFExport._download_s3_field_to_temp(fop_config_field, tmp_dir, prefix="fop_")

            # If there's a logo, download it too so XSL can reference it
            if template_set.logo:
                logo_local = PDFExport._download_s3_field_to_temp(template_set.logo, tmp_dir, prefix="logo_")
                # Inject the logo path into XML so XSL templates can find it
                xml_string = PDFExport.append_element_to_pattern(
                    open(file_with_serialized_xml, 'r', encoding='utf-8').read(),
                    ".",
                    "logo_path",
                    logo_local,
                )
                PDFExport.write_xml_file(xml_string, file_with_serialized_xml)

            PDFExport.perform_xsl_transformation(
                file_with_serialized_xml, xsl_local, fop_config_local, file_output_pdf
            )

        return file_output_pdf
