from __future__ import annotations

from typing import Any

from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CeleryWorkerM2MAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'koalixcrm.auth.m2m_authentication.CeleryWorkerM2MAuthentication'
    name = 'CeleryWorkerM2MAuthentication'

    def get_security_definition(self, auto_schema: Any) -> dict[str, Any]:
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'M2M JWT authentication via Client Credentials Grant.',
        }


class OIDCAccessTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'koalixcrm.auth.oidc_token_authentication.OIDCAccessTokenAuthentication'
    name = 'OIDCAccessTokenAuthentication'

    def get_security_definition(self, auto_schema: Any) -> dict[str, Any]:
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'OIDC access token (JWT) authentication.',
        }
