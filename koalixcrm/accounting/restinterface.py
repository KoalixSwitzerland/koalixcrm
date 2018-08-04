# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework import viewsets
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from koalixcrm.accounting.accounting.account import AccountJSONSerializer
from koalixcrm.accounting.accounting.accounting_period import AccountingPeriodJSONSerializer
from koalixcrm.accounting.accounting.booking import BookingJSONSerializer
from koalixcrm.accounting.accounting.product_categorie import ProductCategoryJSONSerializer
from koalixcrm.accounting.models import Account, AccountingPeriod, Booking, ProductCategorie
from koalixcrm.globalSupportFunctions import ConditionalMethodDecorator
from rest_framework import viewsets

from django.conf import settings


class AccountAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be created, viewed and modified.
    """
    queryset = Account.objects.all()
    serializer_class = AccountJSONSerializer
    filter_fields = ('account_type',)

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(AccountAsJSON, self).dispatch(*args, **kwargs)


class AccountingPeriodAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows accounting periods to be created, viewed and modified.
    """
    queryset = AccountingPeriod.objects.all()
    serializer_class = AccountingPeriodJSONSerializer

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(AccountingPeriodAsJSON, self).dispatch(*args, **kwargs)


class BookingAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be created, viewed and modified.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingJSONSerializer

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(BookingAsJSON, self).dispatch(*args, **kwargs)


class ProductCategoryAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows product categories to be created, viewed and modified.
    """
    queryset = ProductCategorie.objects.all()
    serializer_class = ProductCategoryJSONSerializer

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(ProductCategoryAsJSON, self).dispatch(*args, **kwargs)
