import json
import logging
from urllib.request import urlopen, Request

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .oidc_utils import get_token_auth_header, get_jwks, get_oidc_discovery

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class OIDCAccessTokenAuthentication(BaseAuthentication):
    """
    Validates OIDC access tokens (JWT) from the Authorization header.

    Provider-agnostic: reads OIDC_ISSUER and OIDC_ACCEPTED_AUDIENCES from
    settings. Works with any standard OIDC provider (Cognito, Keycloak, Auth0).

    Maps the token's 'sub' claim to a Django user by email.
    Auto-provisions users on first login if email is available in the token.
    """

    def authenticate(self, request):
        token = get_token_auth_header(request)
        if not token:
            return None

        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.PyJWTError:
            return None

        issuer = getattr(settings, 'OIDC_ISSUER', None)
        if not issuer:
            return None

        accepted_audiences = getattr(settings, 'OIDC_ACCEPTED_AUDIENCES', [])

        jwks = get_jwks(issuer)
        if not jwks:
            raise AuthenticationFailed('Could not retrieve OIDC signing keys.')

        rsa_key = None
        for key in jwks.get('keys', []):
            if key.get('kid') == unverified_header.get('kid'):
                rsa_key = {
                    'kty': key['kty'], 'kid': key['kid'], 'use': key['use'],
                    'n': key['n'], 'e': key['e'],
                }
                break

        if not rsa_key:
            return None

        try:
            signing_key = jwt.PyJWK(rsa_key).key
            payload = jwt.decode(
                token, signing_key,
                algorithms=['RS256'],
                issuer=issuer,
                options={'verify_aud': False},
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access token has expired.')
        except jwt.InvalidTokenError as e:
            logger.debug(f"OIDC JWT claims validation failed: {e}")
            return None
        except jwt.PyJWTError as e:
            raise AuthenticationFailed(f'Invalid access token: {e}')

        # Validate audience
        if accepted_audiences:
            token_aud = payload.get('aud')
            token_client_id = payload.get('client_id')
            token_azp = payload.get('azp')
            aud_set = set(token_aud if isinstance(token_aud, list) else [token_aud]) if token_aud else set()
            if token_client_id:
                aud_set.add(token_client_id)
            if token_azp:
                aud_set.add(token_azp)
            if not aud_set.intersection(accepted_audiences):
                logger.debug(f"OIDC token audience {aud_set} not in accepted {accepted_audiences}")
                return None

        # Map token to Django user
        sub = payload.get('sub')
        if not sub:
            raise AuthenticationFailed('Access token missing sub claim.')

        email = payload.get('email')
        if not email:
            email = self._fetch_email_from_userinfo(issuer, token)

        if not email:
            raise AuthenticationFailed('No email found in access token or userinfo.')

        user = self._find_or_create_user(email, payload)

        if not user.is_active:
            raise AuthenticationFailed('User account is disabled.')

        return (user, payload)

    @staticmethod
    def _fetch_email_from_userinfo(issuer, access_token):
        """Call the OIDC userinfo endpoint to get the user's email."""
        config = get_oidc_discovery(issuer)
        userinfo_endpoint = config.get('userinfo_endpoint') if config else None
        if not userinfo_endpoint:
            return None

        try:
            req = Request(userinfo_endpoint, headers={
                'Authorization': f'Bearer {access_token}',
            })
            with urlopen(req) as resp:
                userinfo = json.loads(resp.read())
                return userinfo.get('email')
        except Exception as e:
            logger.warning(f"Failed to fetch userinfo: {e}")
            return None

    @staticmethod
    def _find_or_create_user(email, payload):
        """Find an existing user by email or auto-provision a new one."""
        try:
            user = UserModel.objects.get(email=email)
            # Sync name if available (never overwrite with empty)
            changed = False
            given_name = payload.get('given_name', '')
            family_name = payload.get('family_name', '')
            if given_name and user.first_name != given_name:
                user.first_name = given_name
                changed = True
            if family_name and user.last_name != family_name:
                user.last_name = family_name
                changed = True
            if changed:
                user.save()
            return user
        except UserModel.DoesNotExist:
            pass

        # Auto-provision new user
        try:
            with transaction.atomic():
                user_data = {
                    'email': email,
                    'first_name': payload.get('given_name', '') or '',
                    'last_name': payload.get('family_name', '') or '',
                }
                if hasattr(UserModel, 'USERNAME_FIELD') and UserModel.USERNAME_FIELD != 'email':
                    user_data[UserModel.USERNAME_FIELD] = email

                user = UserModel.objects.create_user(**user_data)
                logger.info(f"Auto-provisioned new user {email} from OIDC access token")
                return user
        except IntegrityError as e:
            logger.error(f"Failed to auto-provision user {email}: {e}")
            raise AuthenticationFailed('Failed to create user from access token.')
