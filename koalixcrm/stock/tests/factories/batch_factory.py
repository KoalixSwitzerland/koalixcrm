# -*- coding: utf-8 -*-
import datetime

import factory

from koalixcrm.stock.models.batch import Batch
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory


class StandardBatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Batch

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    variant = factory.SubFactory(StandardProductVariantFactory)
    batch_number = factory.Sequence(lambda n: f"BATCH-{n}")
    expiry_date = factory.LazyFunction(lambda: datetime.date.today() + datetime.timedelta(days=30))
    production_date = factory.LazyFunction(lambda: datetime.date.today() - datetime.timedelta(days=1))
    quarantine = False
