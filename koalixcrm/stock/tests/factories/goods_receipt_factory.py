# -*- coding: utf-8 -*-
import factory
from django.utils import timezone

from koalixcrm.stock.models.goods_receipt import GoodsReceipt
from koalixcrm.stock.models.goods_receipt_line import GoodsReceiptLine
from koalixcrm.contacts.tests.factories.contact_factory import StandardContactFactory
from koalixcrm.core.tests.factories.unit_factory import StandardUnitFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory
from koalixcrm.products.tests.factories.product_variant_factory import StandardProductVariantFactory


class StandardGoodsReceiptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoodsReceipt

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    supplier_party = factory.SubFactory(StandardContactFactory)
    external_doc_ref = factory.Sequence(lambda n: f"DN-{n}")
    received_at = factory.LazyFunction(timezone.now)


class StandardGoodsReceiptLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoodsReceiptLine

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    goods_receipt = factory.SubFactory(StandardGoodsReceiptFactory)
    variant = factory.SubFactory(StandardProductVariantFactory)
    expected_qty = "10.0000"
    received_qty = "0.0000"
    uom = factory.SubFactory(StandardUnitFactory)
