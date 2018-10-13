# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets

from koalixcrm.accounting.models import Account, AccountingPeriod, Booking, ProductCategory
from koalixcrm.accounting.rest.account_rest import AccountJSONSerializer
from koalixcrm.accounting.rest.accounting_period_rest import AccountingPeriodJSONSerializer
from koalixcrm.accounting.rest.booking_rest import BookingJSONSerializer
from koalixcrm.accounting.rest.product_categorie_rest import ProductCategoryJSONSerializer
from koalixcrm.global_support_functions import ConditionalMethodDecorator


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
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryJSONSerializer

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(ProductCategoryAsJSON, self).dispatch(*args, **kwargs)
