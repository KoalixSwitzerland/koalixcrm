# -*- coding: utf-8 -*-

import factory
from koalixcrm.djangoUserExtension.models import TemplateSet


class StandardTemplateSetFactory(factory.Factory):
    class Meta:
        model = TemplateSet

    title = "Just an empty Template Set"
