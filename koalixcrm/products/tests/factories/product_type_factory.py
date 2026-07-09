# -*- coding: utf-8 -*-

import datetime

import factory

from koalixcrm.global_support_functions import make_date_utc
from koalixcrm.products.models.choices import ProductKind
from koalixcrm.products.models.product import Product
from tests.factories.contacts.user_factory import StaffUserFactory
from tests.factories.core.tax_factory import StandardTaxFactory
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory


class StandardProductTypeFactory(factory.django.DjangoModelFactory):
    """Builds `products.Product` (renamed from `ProductType` — ADR-0003
    Amendment 2026-06-27). Factory class name kept stable for the many
    existing test call sites; only the underlying model and field names
    changed (`default_unit` -> `base_uom`, `tax` -> `tax_class`)."""

    class Meta:
        model = Product
        django_get_or_create = ('product_type_identifier',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    title = "This is a test Product"
    description = "This is a test Product"
    product_type_identifier = "123456"
    kind = ProductKind.TRADING_GOOD
    base_uom = factory.SubFactory(StandardUnitFactory)
    date_of_creation = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    last_modification = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    last_modified_by = factory.SubFactory(StaffUserFactory)
    tax_class = factory.SubFactory(StandardTaxFactory)
