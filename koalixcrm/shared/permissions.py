# -*- coding: utf-8 -*-
"""
Shared permission classes for koalixcrm REST API.
"""
from rest_framework import permissions


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
