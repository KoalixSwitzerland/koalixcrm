# -*- coding: utf-8 -*-
"""
Contract Object Management API entry point.

Exposes Contract/Document REST viewsets for URL routing.
"""
from koalixcrm.contract_object_management.views.contract_view_set import ContractViewSet

__all__ = [
    'ContractViewSet',
]
