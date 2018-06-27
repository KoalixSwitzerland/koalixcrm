# -*- coding: utf-8 -*-
from koalixcrm.accounting.models import Account, AccountJSONSerializer
from rest_framework import viewsets


class AccountAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be created, viewed and modified.
    """
    queryset = Account.objects.all()
    serializer_class = AccountJSONSerializer
