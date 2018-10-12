# -*- coding: utf-8 -*-

import factory
import datetime
from koalixcrm.crm.models import Product
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory
from koalixcrm.crm.factories.factory_user import StaffUserFactory
from koalixcrm.accounting.factories.factory_product_category import StandardProductCategoryFactory
from koalixcrm.test_support_functions import make_date_utc


class StandardProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('product_number',)
