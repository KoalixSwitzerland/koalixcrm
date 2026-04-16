# -*- coding: utf-8 -*-
"""
Provides XML rendering support.
"""

import os
import tempfile
from subprocess import check_output, STDOUT
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer

from koalixcrm.core.documents.pdf_export import PDFExport


class XSLFORenderer(TemplateHTMLRenderer):
    """
    Renderer which serializes to PDF using XSLT and FO
    """
    media_type_unused = 'application/pdf'
    media_type = 'plain/text'
    format = 'pdf'
    charset = 'utf-8'

    def get_template_names(self, response, view):
        """Override with xslt_names. This allows for you
        to still render HTML if you want
        """
        if hasattr(response, 'xslt_name'):
            return [response.latex_name]
        elif self.xslt_name:
            return [self.xslt_name]
        elif hasattr(view, 'get_xslt_names'):
            return view.get_xslt_names()
        elif hasattr(view, 'xslt_name'):
            return [view.xslt_name]
        raise ImproperlyConfigured(
            u'Returned a template response with no `xslt_name` attribute '
            u'set on either the view or response')

    def perform_xsl_transformation(self, file_with_serialized_xml, xsl_file, fop_config_file, file_output_pdf):
        with tempfile.TemporaryDirectory(prefix="koalixcrm_fop_") as tmp_dir:
            xsl_local = PDFExport._download_s3_field_to_temp(xsl_file, tmp_dir, prefix="xsl_")
            fop_local = PDFExport._download_s3_field_to_temp(fop_config_file, tmp_dir, prefix="fop_")
            PDFExport.perform_xsl_transformation(
                file_with_serialized_xml, xsl_local, fop_local, file_output_pdf
            )

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        First renders `data` into serialized XML, afterwards start fop and return PDF
        """
        if data is None:
            return ''

        super(XSLFORenderer, self).render(data, accepted_media_type, renderer_context)

        xml_renderer = XMLRenderer()
        xml_string = xml_renderer.render(data, accepted_media_type, renderer_context)
        xml_file = open(renderer_context['view'].file_name, "wb+")
        xml_file.truncate()
        xml_file.write(xml_string.encode('utf-8'))
        xml_file.close()
        # perform xsl transformation
        self.perform_xsl_transformation(xml_file,
                                        self.xsl_file,
                                        self.fop_config_file,
                                        self.file_output_pdf)

        # Read file
        with open(self.file_output_pdf, 'rb') as f:
            rendered_output = f.read()

        return rendered_output