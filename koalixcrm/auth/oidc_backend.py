import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction

from .oidc_utils import validate_jwt

logger = logging.getLogger(__name__)
UserModel = get_user_model()


def _sync_groups_from_provider(user, claims):
    """
    Additively sync groups from OIDC provider claims to Django groups.

    Existing Django group assignments are never removed.

    Supported claim locations:
    - 'cognito:groups' (Cognito)
    - 'groups' (Keycloak mapper or other providers)
    - 'realm_access.roles' (Keycloak default)
    """
    provider_groups = (
        claims.get('cognito:groups')
        or claims.get('groups')
        or (claims.get('realm_access') or {}).get('roles')
        or []
    )
    if not provider_groups:
        return

    if isinstance(provider_groups, str):
        provider_groups = [provider_groups]

    existing_groups = set(user.groups.values_list('name', flat=True))
    groups_to_add = set(provider_groups) - existing_groups
    if not groups_to_add:
        return

    for group_name in groups_to_add:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

    logger.info(f"Added groups {groups_to_add} to user {user.email} from provider claims")


class OIDCAuthenticationBackend:
    """
    Django authentication backend for OIDC.

    Handles user creation and identity linking via email.
    Groups from the provider are additively merged into Django groups.
    """

    def authenticate(self, request, provider=None, user_info=None, id_token=None, **kwargs):
        if provider and user_info:
            return self._authenticate_with_user_info(provider, user_info)

        if id_token:
            return self._authenticate_with_id_token(id_token, **kwargs)

        return None

    def _authenticate_with_user_info(self, provider, user_info):
        """Authenticate using standardized user info from any OAuth provider."""
        user_email = user_info.get('email')
        if not user_email:
            logger.error(f"User info missing 'email' for provider {provider}.")
            return None

        try:
            with transaction.atomic():
                user = self._find_or_create_user(user_email, user_info)
                if user is None:
                    return None

                given_name = user_info.get('given_name', '')
                family_name = user_info.get('family_name', '')
                if given_name:
                    user.first_name = given_name
                if family_name:
                    user.last_name = family_name
                user.save()

                _sync_groups_from_provider(user, user_info)

            return user
        except Exception as e:
            logger.error(f"Authentication error for {provider} user {user_email}: {e}", exc_info=True)
            return None

    def _authenticate_with_id_token(self, id_token, **kwargs):
        """Legacy authentication path using JWT validation."""
        access_token = kwargs.get('access_token')

        try:
            from django.conf import settings
            issuer = getattr(settings, 'OIDC_ISSUER', None)
            if not issuer:
                return None

            payload = validate_jwt(id_token, authority_url=issuer, access_token=access_token)

            user_info = {
                'email': payload.get('email'),
                'given_name': payload.get('given_name', ''),
                'family_name': payload.get('family_name', ''),
                'cognito:groups': payload.get('cognito:groups', []),
                'groups': payload.get('groups', []),
                'realm_access': payload.get('realm_access', {}),
            }

            return self._authenticate_with_user_info('oidc', user_info)
        except Exception as e:
            logger.error(f"OIDC Authentication Error: {e}", exc_info=True)
            return None

    @staticmethod
    def _find_or_create_user(email, user_info):
        """Find an existing user by email or create a new one."""
        try:
            return UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            pass

        try:
            user_data = {
                'email': email,
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', ''),
            }
            if hasattr(UserModel, 'USERNAME_FIELD') and UserModel.USERNAME_FIELD != 'email':
                user_data[UserModel.USERNAME_FIELD] = email

            user = UserModel.objects.create_user(**user_data)
            logger.info(f"Created new user {email} via OIDC")
            return user
        except IntegrityError as e:
            logger.error(f"Could not create user for email {email}: {str(e)}")
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
