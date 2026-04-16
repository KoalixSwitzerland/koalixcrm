# -*- coding: utf-8 -*-

import factory
from koalixcrm.accounting.models import Account


class StandardAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account
        django_get_or_create = ('account_number',)

    account_number = 1000
    title = "Cash"
    account_type = "A"
    description = "This is a test cash account"
    is_open_reliabilities_account = False
    is_open_interest_account = False
    is_product_inventory_activa = False
    is_a_customer_payment_account = False


class OpenReliabilitiesAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account
        django_get_or_create = ('account_number',)

    account_number = 2000
    title = "Open Reliabilities"
    account_type = "L"
    description = "This is a test open reliabilities account"
    is_open_reliabilities_account = True
    is_open_interest_account = False
    is_product_inventory_activa = False
    is_a_customer_payment_account = False


class OpenInterestAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account
        django_get_or_create = ('account_number',)

    account_number = 1100
    title = "Open Interest"
    account_type = "A"
    description = "This is a test open interest account"
    is_open_reliabilities_account = False
    is_open_interest_account = True
    is_product_inventory_activa = False
    is_a_customer_payment_account = False
