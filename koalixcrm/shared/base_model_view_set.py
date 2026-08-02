# -*- coding: utf-8 -*-
"""
Base ViewSet for all koalixcrm REST API endpoints.
"""
from __future__ import annotations

from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from koalixcrm.shared.filters import AutoFilterBackend
from koalixcrm.shared.permissions import ModelPermissionsWithListView


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet providing standard authentication, permissions, and filtering.
    All app-specific ViewSets should inherit from this class.
    """
    permission_classes = [IsAuthenticated, ModelPermissionsWithListView]
    # This list overrides DEFAULT_FILTER_BACKENDS rather than extending it, so
    # `AutoFilterBackend` has to be named here explicitly: leaving it out does
    # not fall back to the project default, it silently disables field
    # filtering everywhere, and an unknown query parameter is then ignored
    # rather than rejected. `test_filtering.py` guards this.
    filter_backends = [AutoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
