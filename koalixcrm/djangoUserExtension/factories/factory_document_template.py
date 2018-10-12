# -*- coding: utf-8 -*-

import factory
from koalixcrm.djangoUserExtension.models import QuoteTemplate
from filebrowser.base import FileObject


class StandardQuoteTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuoteTemplate

    title = "This is a test Quote Template"
    xsl_file = FileObject("~/path/to/xsl_file.xsl")
    fop_config_file = FileObject("~/path/to/fop_config_file.xml")
    logo = FileObject("~/path/to/logo_file.jpg")
