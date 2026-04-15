# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.contracts.models.purchase_confirmation import PurchaseConfirmation
from koalixcrm.contracts.serializers.purchase_confirmation_serializer import PurchaseConfirmationJSONSerializer


class PurchaseConfirmationViewSet(BaseModelViewSet):
    queryset = PurchaseConfirmation.objects.all()
    serializer_class = PurchaseConfirmationJSONSerializer
