# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.accounting.models import Account
from koalixcrm.accounting.serializers.account_serializer import AccountJSONSerializer


class AccountViewSet(BaseModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountJSONSerializer
