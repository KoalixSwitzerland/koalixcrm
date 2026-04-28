# -*- coding: utf-8 -*-
"""
Base ViewSet for all koalixcrm REST API endpoints.
"""
from __future__ import annotations

from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from koalixcrm.shared.permissions import ModelPermissionsWithListView


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet providing standard authentication, permissions, and filtering.
    All app-specific ViewSets should inherit from this class.
    """
    permission_classes = [IsAuthenticated, ModelPermissionsWithListView]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
