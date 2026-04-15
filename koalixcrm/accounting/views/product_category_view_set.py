# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.accounting.models import ProductCategory
from koalixcrm.accounting.serializers.product_category_serializer import ProductCategoryJSONSerializer


class ProductCategoryViewSet(BaseModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryJSONSerializer
