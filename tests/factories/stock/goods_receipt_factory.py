# -*- coding: utf-8 -*-
import factory
from django.utils import timezone

from koalixcrm.stock.models.goods_receipt import GoodsReceipt
from koalixcrm.stock.models.goods_receipt_line import GoodsReceiptLine
from tests.factories.contacts.contact_factory import StandardContactFactory
from tests.factories.core.unit_factory import StandardUnitFactory
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory
from tests.factories.products.product_variant_factory import StandardProductVariantFactory


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
