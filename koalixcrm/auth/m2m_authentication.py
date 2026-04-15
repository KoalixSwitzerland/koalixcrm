import logging

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .oidc_utils import get_token_auth_header, validate_jwt

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class CeleryWorkerM2MAuthentication(BaseAuthentication):
    """
    Authenticates M2M clients (Client Credentials Grant) via a JWT.

    Validates the token against CELERY_WORKER_M2M_OIDC_ISSUER and maps
    the client_id claim to a Django service user by username.
    """

    def authenticate(self, request):
        token = get_token_auth_header(request)
        if not token:
            return None

        try:
            jwt.get_unverified_header(token)
        except jwt.PyJWTError:
            return None

        try:
            authority_url = getattr(settings, 'CELERY_WORKER_M2M_OIDC_ISSUER', None)
            if not authority_url:
                return None

            # Check if this token was issued by the M2M authority
            try:
                unverified_claims = jwt.decode(
                    token, algorithms=["RS256"],
                    options={"verify_signature": False},
                )
                if unverified_claims.get('iss') != authority_url:
                    return None

                # Verify client identity matches M2M client
                m2m_client_id = getattr(settings, 'CELERY_WORKER_M2M_CLIENT_ID', None)
                token_azp = unverified_claims.get('azp')
                token_client_id = unverified_claims.get('client_id')
                if m2m_client_id and token_azp != m2m_client_id and token_client_id != m2m_client_id:
                    return None
            except jwt.PyJWTError:
                return None

            # Full signature validation
            payload = validate_jwt(token, authority_url=authority_url, client_id=None)

            client_id = payload.get('client_id') or payload.get('azp')
            if not client_id:
                raise AuthenticationFailed(
                    "M2M token is missing client identifier (checked 'client_id' and 'azp' claims)."
                )

            # Map M2M client to a Django service user by username
            try:
                user = UserModel.objects.get(username=client_id)
            except UserModel.DoesNotExist:
                # Auto-provision a service user for this M2M client
                user = UserModel.objects.create_user(
                    username=client_id,
                    email=f'{client_id}@m2m.local',
                    is_active=True,
                )
                logger.info(f"Auto-provisioned M2M service user: {client_id}")

            if not user.is_active:
                raise AuthenticationFailed('This service account is disabled.')

            return (user, payload)

        except AuthenticationFailed:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during M2M authentication: {e}", exc_info=True)
            raise AuthenticationFailed("M2M token authentication failed.")
