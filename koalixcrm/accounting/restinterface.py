# -*- coding: utf-8 -*-
from koalixcrm.accounting.models import Account, AccountJSONSerializer, ACCOUNTTYPECHOICES, ProductCategorie, \
    ProductCategoryJSONSerializer
from rest_framework import viewsets


class AccountAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be created, viewed and modified.
    """
    queryset = Account.objects.all()
    serializer_class = AccountJSONSerializer
    filter_fields = ('account_type',)


class ProductCategoryAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows product categories to be created, viewed and modified.
    """
    queryset = ProductCategorie.objects.all()
    serializer_class = ProductCategoryJSONSerializer
