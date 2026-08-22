# -*- coding: utf-8 -*-
"""
Read-only ViewSet for :class:`UserExtension`.

The PDF worker fetches this aggregate to render the issuing user's company
block in the XSL-FO document.
"""
from __future__ import annotations

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from koalixcrm.djangoUserExtension.models.user_extension import UserExtension
from koalixcrm.djangoUserExtension.serializers.user_extension_nested import (
    UserExtensionNestedSerializer,
)
from koalixcrm.shared.permissions import ModelPermissionsWithListView
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin


class UserExtensionViewSet(
    WorkspaceScopedViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = UserExtension.objects.all()
    serializer_class = UserExtensionNestedSerializer
    permission_classes = [IsAuthenticated, ModelPermissionsWithListView]
    http_method_names = ["get", "head", "options"]
