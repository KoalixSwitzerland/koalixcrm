# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from koalixcrm.accounting.models import Account, AccountingPeriod, Booking, ProductCategory
from koalixcrm.accounting.rest.account_rest import AccountJSONSerializer
from koalixcrm.accounting.rest.accounting_period_rest import AccountingPeriodJSONSerializer
from koalixcrm.accounting.rest.booking_rest import BookingJSONSerializer
from koalixcrm.accounting.rest.product_categorie_rest import ProductCategoryJSONSerializer


class AccountAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be created, viewed and modified.
    """
    queryset = Account.objects.all()
    serializer_class = AccountJSONSerializer
    filter_fields = ('account_type',)

    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((IsAuthenticated,))
    def dispatch(self, *args, **kwargs):
        return super(AccountAsJSON, self).dispatch(*args, **kwargs)


class AccountingPeriodAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows accounting periods to be created, viewed and modified.
    """
    queryset = AccountingPeriod.objects.all()
    serializer_class = AccountingPeriodJSONSerializer

    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((IsAuthenticated,))
    def dispatch(self, *args, **kwargs):
        return super(AccountingPeriodAsJSON, self).dispatch(*args, **kwargs)


class BookingAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be created, viewed and modified.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingJSONSerializer

    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((IsAuthenticated,))
    def dispatch(self, *args, **kwargs):
        return super(BookingAsJSON, self).dispatch(*args, **kwargs)


class ProductCategoryAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows product categories to be created, viewed and modified.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryJSONSerializer

    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((IsAuthenticated,))
    def dispatch(self, *args, **kwargs):
        return super(ProductCategoryAsJSON, self).dispatch(*args, **kwargs)
