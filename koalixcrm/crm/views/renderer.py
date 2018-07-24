# -*- coding: utf-8 -*-
"""
Provides XML rendering support.
"""
from django.core.exceptions import ImproperlyConfigured
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer


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
        elif self.latex_name:
            return [self.latex_name]
        elif hasattr(view, 'get_xslt_names'):
            return view.get_latex_names()
        elif hasattr(view, 'xslt_name'):
            return [view.latex_name]
        raise ImproperlyConfigured(
            u'Returned a template response with no `xslt_name` attribute '
            u'set on either the view or response')

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        First renders `data` into serialized XML, afterwards start fop and return PDF
        """
        if data is None:
            return ''

        super(XSLFORenderer, self).render(data, accepted_media_type, renderer_context)

        xml_renderer = XMLRenderer()
        xml_string = xml_renderer.render(data, accepted_media_type, renderer_context)
        f = open(renderer_context['view'].file_name, "wb+")
        f.truncate()
        f.write(xml_string.encode('utf-8'))
        f.close()

        return renderer_context['view'].__str__()