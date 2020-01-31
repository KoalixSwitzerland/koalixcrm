# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Marcos Pereira <marcospereira.mpj@gmail.com>
# Modified by Sairam Krish <haisairam@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import re

from django.conf import settings
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakInvalidTokenError
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotAuthenticated

logger = logging.getLogger(__name__)


class KeycloakMiddleware(MiddlewareMixin):

    """
        Constructor
        :param get_response: Callable that takes the request and returns a response
    """
    def __init__(self, get_response):


        self.config = settings.KEYCLOAK_CONFIG

        # Read configurations
        try:
            self.server_url = self.config['KEYCLOAK_SERVER_URL']
            self.client_id = self.config['KEYCLOAK_CLIENT_ID']
            self.realm = self.config['KEYCLOAK_REALM']
        except KeyError as e:
            raise Exception("KEYCLOAK_SERVER_URL, KEYCLOAK_CLIENT_ID or KEYCLOAK_REALM not found.")

        self.client_secret_key = self.config.get('KEYCLOAK_CLIENT_SECRET_KEY', None)
        self.client_public_key = self.config.get('KEYCLOAK_CLIENT_PUBLIC_KEY', None)
        self.default_access = self.config.get('KEYCLOAK_DEFAULT_ACCESS', "DENY")
        self.method_validate_token = self.config.get('KEYCLOAK_METHOD_VALIDATE_TOKEN', "INTROSPECT")
        self.keycloak_authorization_config = self.config.get('KEYCLOAK_AUTHORIZATION_CONFIG', None)

        # Create Keycloak instance
        self.keycloak = KeycloakOpenID(server_url=self.server_url,
                                       client_id=self.client_id,
                                       realm_name=self.realm,
                                       client_secret_key=self.client_secret_key)

        # Read policies
        if self.keycloak_authorization_config:
            self.keycloak.load_authorization_config(self.keycloak_authorization_config)

        # Django
        self.get_response = get_response

    @property
    def keycloak(self):
        return self._keycloak

    @keycloak.setter
    def keycloak(self, value):
        self._keycloak = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def server_url(self):
        return self._server_url

    @server_url.setter
    def server_url(self, value):
        self._server_url = value

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def client_secret_key(self):
        return self._client_secret_key

    @client_secret_key.setter
    def client_secret_key(self, value):
        self._client_secret_key = value

    @property
    def client_public_key(self):
        return self._client_public_key

    @client_public_key.setter
    def client_public_key(self, value):
        self._client_public_key = value

    @property
    def realm(self):
        return self._realm

    @realm.setter
    def realm(self, value):
        self._realm = value

    @property
    def keycloak_authorization_config(self):
        return self._keycloak_authorization_config

    @keycloak_authorization_config.setter
    def keycloak_authorization_config(self, value):
        self._keycloak_authorization_config = value

    @property
    def method_validate_token(self):
        return self._method_validate_token

    @method_validate_token.setter
    def method_validate_token(self, value):
        self._method_validate_token = value

    def __call__(self, request):
        """
        :param request:
        :return:
        """
        return self.get_response(request)

    """
        Validate only the token introspect.
        :param request: django request
        :param view_func:
        :param view_args: view args
        :param view_kwargs: view kwargs
        :return:
    """
    def process_view(self, request, view_func, view_args, view_kwargs):


        if hasattr(settings, 'KEYCLOAK_BEARER_AUTHENTICATION_EXEMPT_PATHS'):
            path = request.path_info.lstrip('/')

            if any(re.match(m, path) for m in
                   settings.KEYCLOAK_BEARER_AUTHENTICATION_EXEMPT_PATHS):
                logger.debug('** exclude path found, skipping')
                return None

        try:
            view_scopes = view_func.cls.keycloak_scopes
        except AttributeError as e:
            logger.debug(
                'Allowing free acesss, since no authorization configuration (keycloak_scopes) found for this request route :%s',
                request)
            return None

        if 'HTTP_AUTHORIZATION' not in request.META:
            return JsonResponse({"detail": NotAuthenticated.default_detail},
                                status=NotAuthenticated.status_code)

        auth_header = request.META.get('HTTP_AUTHORIZATION').split()
        token = auth_header[1] if len(auth_header) == 2 else auth_header[0]

        # Get default if method is not defined.
        required_scope = view_scopes.get(request.method, None) \
            if view_scopes.get(request.method, None) else view_scopes.get('DEFAULT', None)

        # DEFAULT scope not found and DEFAULT_ACCESS is DENY
        if not required_scope and self.default_access == 'DENY':
            return JsonResponse({"detail": PermissionDenied.default_detail},
                                status=PermissionDenied.status_code)

        try:
            user_permissions = self.keycloak.get_permissions(token,
                                                             method_token_info=self.method_validate_token.lower(),
                                                             key=self.client_public_key)
        except KeycloakInvalidTokenError as e:
            return JsonResponse({"detail": AuthenticationFailed.default_detail},
                                status=AuthenticationFailed.status_code)

        for perm in user_permissions:
            if required_scope in perm.scopes:
                return None

        # User Permission Denied
        return JsonResponse({"detail": PermissionDenied.default_detail},
                            status=PermissionDenied.status_code)
