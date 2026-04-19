# -*- coding: utf-8 -*-
"""
Read-only ViewSet for :class:`UserExtension`.

The PDF worker fetches this aggregate to render the issuing user's company
block in the XSL-FO document.
"""
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from koalixcrm.djangoUserExtension.models.user_extension import UserExtension
from koalixcrm.djangoUserExtension.serializers.user_extension_nested import (
    UserExtensionNestedSerializer,
)
from koalixcrm.shared.permissions import ModelPermissionsWithListView


class UserExtensionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = UserExtension.objects.all()
    serializer_class = UserExtensionNestedSerializer
    permission_classes = [IsAuthenticated, ModelPermissionsWithListView]
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        active = getattr(self.request, 'active_workspace', None)
        if self.request.user.is_superuser:
            return UserExtension.objects.all()
        if active is None:
            return UserExtension.objects.none()
        return UserExtension.objects.filter(workspace=active)

    def perform_create(self, serializer):
        from koalixcrm.core.models.workspace import Workspace
        active = getattr(self.request, 'active_workspace', None)
        if active is None and self.request.user.is_superuser:
            active, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True}
            )
        serializer.save(workspace=active)
