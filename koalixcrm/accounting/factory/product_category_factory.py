# -*- coding: utf-8 -*-

import factory
from koalixcrm.accounting.models import ProductCategory


class StandardProductCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductCategory
        django_get_or_create = ('title',)

    title = "Service"
    profit_account = ""
    loss_account = ""
