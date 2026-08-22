# -*- coding: utf-8 -*-
"""
Shared permission classes for koalixcrm REST API.
"""
from __future__ import annotations

from rest_framework import permissions


class WorkspaceMembershipPermission(permissions.BasePermission):
    """Require a role in the workspace named by the URL ``workspace_id`` kwarg.

    Org ADR-0008 line 3 / org ADR-0013 layer 0, specified by REQ-0028.

    Django model permissions are organisation-wide: they answer "may this user
    touch invoices at all", never "may they touch *this tenant's* invoices".
    Without this class the ``<int:workspace_id>`` path segment — which is
    caller-controlled — is accepted verbatim, and any authenticated user with
    ordinary model rights reaches any tenant's rows by editing one path
    segment.

    Routes whose URL resolution yields no ``workspace_id`` kwarg pass through
    untouched: those are the deliberately cross-workspace and platform-wide
    surfaces.

    Must be combined with, not substituted for, the model-permission class:
    this answers *which tenant*, that answers *which model*.
    """

    message = 'You do not have a role in this workspace.'

    def has_permission(self, request, view) -> bool:
        workspace_id = (getattr(view, 'kwargs', None) or {}).get('workspace_id')
        if workspace_id is None:
            return True

        # `roles_in_workspace` already covers superusers and the service
        # account, and already fails closed on a missing or inactive
        # workspace, so neither needs a special case here.
        from koalixcrm.core.access import roles_in_workspace

        return bool(roles_in_workspace(request.user, workspace_id))


class ModelPermissionsWithListView(permissions.DjangoModelPermissions):
    """
    Extends DjangoModelPermissions to also check for the 'view' permission
    on GET requests (list and detail views).
    """

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ReadModelPermissions(permissions.DjangoModelPermissions):
    """Require the ``view`` model permission whatever the HTTP method is.

    For read-only endpoints whose lookup is expressed as a POST because the
    query does not fit in a URL (a scanned code, an availability window).
    ``DjangoModelPermissions`` would map that POST to ``add_<model>`` and so
    demand a write right for a pure read.

    The model is taken from the view's ``queryset`` as usual, so an APIView
    using this must declare one (``Model.objects.none()`` is enough — the
    queryset is only read for its ``.model``).
    """

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.view_%(model_name)s'],
        'PUT': ['%(app_label)s.view_%(model_name)s'],
        'PATCH': ['%(app_label)s.view_%(model_name)s'],
        'DELETE': ['%(app_label)s.view_%(model_name)s'],
    }
