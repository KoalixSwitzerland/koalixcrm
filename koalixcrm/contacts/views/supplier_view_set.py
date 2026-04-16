# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contacts.models.supplier import Supplier
from koalixcrm.contacts.serializers.supplier_serializer import SupplierJSONSerializer


class SupplierViewSet(BaseModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierJSONSerializer
