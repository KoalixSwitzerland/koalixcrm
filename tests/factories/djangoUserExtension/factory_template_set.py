# -*- coding: utf-8 -*-

import factory
from koalixcrm.djangoUserExtension.models import TemplateSet


class StandardTemplateSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TemplateSet

    title = "Just an empty Template Set"
