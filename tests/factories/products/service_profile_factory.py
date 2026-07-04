# -*- coding: utf-8 -*-

import factory

from koalixcrm.products.models.choices import ProductKind, ServiceBillingModel
from koalixcrm.products.models.service_profile import ServiceProfile
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_type_factory import StandardProductTypeFactory


class StandardServiceProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ServiceProfile
        django_get_or_create = ('product',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    product = factory.SubFactory(
        StandardProductTypeFactory,
        kind=ProductKind.SERVICE,
        product_type_identifier=factory.Sequence(lambda n: f"SERVICE-{n}"),
    )
    billing_model = ServiceBillingModel.HOURLY
    default_duration = 60
    deliverable = "Standard consulting deliverable"
    sla_reference = "SLA-001"
