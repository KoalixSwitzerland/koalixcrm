# -*- coding: utf-8 -*-
"""
CRM API entry point.

Exposes all CRM REST viewsets for URL routing.
"""
from koalixcrm.crm.serializers.restinterface import (
    ContractAsJSON,
    CurrencyAsJSON,
    ProductAsJSON,
    ProjectAsJSON,
    TaskAsJSON,
    TaskStatusAsJSON,
    TaxAsJSON,
    UnitAsJSON,
    CustomerGroupAsJSON,
    CustomerBillingCycleAsJSON,
    CustomerAsJSON,
    ContactPostalAddressAsJSON,
    ContactEmailAddressAsJSON,
    ContactPhoneAddressAsJSON,
    ProjectStatusAsJSON,
    AgreementAsJSON,
)

__all__ = [
    'ContractAsJSON',
    'CurrencyAsJSON',
    'ProductAsJSON',
    'ProjectAsJSON',
    'TaskAsJSON',
    'TaskStatusAsJSON',
    'TaxAsJSON',
    'UnitAsJSON',
    'CustomerGroupAsJSON',
    'CustomerBillingCycleAsJSON',
    'CustomerAsJSON',
    'ContactPostalAddressAsJSON',
    'ContactEmailAddressAsJSON',
    'ContactPhoneAddressAsJSON',
    'ProjectStatusAsJSON',
    'AgreementAsJSON',
]
