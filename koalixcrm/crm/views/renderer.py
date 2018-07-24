# -*- coding: utf-8 -*-
"""
Provides XML rendering support.
"""
from __future__ import unicode_literals

from rest_framework.renderers import BaseRenderer
from rest_framework_xml.renderers import XMLRenderer


class PDFRenderer(BaseRenderer):
    """
    Renderer which serializes to PDF using FOP
    """
    media_type_unused = 'application/pdf'
    media_type = 'plain/text'
    format = 'pdf'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        First renders `data` into serialized XML, afterwards start fop and return PDF
        """
        if data is None:
            return ''
        xml_renderer = XMLRenderer()
        xml_string = xml_renderer.render(data, accepted_media_type, renderer_context)
        f = open(renderer_context['view'].file_name, "wb+")
        f.truncate()
        f.write(xml_string.encode('utf-8'))
        f.close()
        return renderer_context['view'].__str__()