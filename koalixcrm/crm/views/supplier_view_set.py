# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.crm.contact.supplier import Supplier
from koalixcrm.crm.serializers.supplier_serializer import SupplierJSONSerializer


class SupplierViewSet(BaseModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierJSONSerializer
