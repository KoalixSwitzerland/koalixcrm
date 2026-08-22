from __future__ import annotations

import logging
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, Group
from django.db import IntegrityError, transaction
from django.http import HttpRequest

from .oidc_utils import validate_jwt

logger = logging.getLogger(__name__)
UserModel = get_user_model()

#: Namespace prefix for every group derived from an IdP claim (koalixcrm#430).
OIDC_GROUP_PREFIX = 'oidc'


def _sync_groups_from_provider(
    user: AbstractBaseUser, claims: dict[str, Any], issuer: str | None
) -> None:
    """
    Additively sync groups from OIDC provider claims to Django groups.

    koalixcrm#430: every claim value is namespaced unconditionally as
    ``oidc:<tenantAlias>:<claimValue>`` — never the raw claim value, and never
    with a special case for any particular claim value. A claim can therefore
    no longer syntactically name a locally meaningful group (notably the one
    in ``settings.M2M_MICROSERVICE_GROUP_NAME``), whatever it contains, so no
    allow-list, deny-list or sanitisation is needed to keep that property.

    ``tenantAlias`` comes exclusively from ``core.OidcTenant.alias``, resolved
    by ``issuer`` — the already-validated token issuer — never from claim
    content. If no ``OidcTenant`` matches ``issuer`` (or no issuer was
    established at all), the sync is skipped entirely for this request: no
    group is created, no membership changed, no exception raised — the
    caller's authentication continues on the user's pre-existing groups.
    Registering the tenant row *is* the per-issuer opt-in.

    Existing Django group assignments are never removed — Django remains the
    authoritative source for group management.

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

    if not issuer:
        logger.info(
            "No validated issuer available for this request — skipping group sync."
        )
        return

    from koalixcrm.core.models.oidc_tenant import OidcTenant

    tenant = OidcTenant.objects.filter(issuer=issuer).first()
    if tenant is None:
        logger.info(
            "No core.OidcTenant registered for validated issuer %r — "
            "skipping group sync for this request.", issuer,
        )
        return

    namespaced_names = {f'{OIDC_GROUP_PREFIX}:{tenant.alias}:{value}' for value in provider_groups}
    existing_groups = set(user.groups.values_list('name', flat=True))
    groups_to_add = namespaced_names - existing_groups
    if not groups_to_add:
        return

    for group_name in groups_to_add:
        group, _created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

    logger.info(
        "Added groups %s to user %s from provider claims (tenant=%s)",
        groups_to_add, user.email, tenant.alias,
    )


class OIDCAuthenticationBackend:
    """
    Django authentication backend for OIDC.

    Handles user creation and identity linking via email.
    Groups from the provider are additively merged into Django groups.
    """

    def authenticate(
        self,
        request: HttpRequest | None,
        provider: str | None = None,
        user_info: dict[str, Any] | None = None,
        id_token: str | None = None,
        **kwargs: Any,
    ) -> AbstractBaseUser | None:
        if provider and user_info:
            # The interactive path is served by `oidc_views`, whose authlib
            # client is configured from ADMIN_OIDC_ISSUER's discovery
            # document — so that is the issuer this token was validated
            # against (koalixcrm#430).
            from django.conf import settings

            return self._authenticate_with_user_info(
                provider, user_info, validated_issuer=getattr(settings, 'ADMIN_OIDC_ISSUER', None)
            )

        if id_token:
            return self._authenticate_with_id_token(id_token, **kwargs)

        return None

    def _authenticate_with_user_info(
        self, provider: str, user_info: dict[str, Any], validated_issuer: str | None = None
    ) -> AbstractBaseUser | None:
        """Authenticate using standardized user info from any OAuth provider.

        ``validated_issuer`` is the issuer this caller actually validated the
        token against. It is required for group synchronisation and must never
        be taken from the claims themselves — see
        :func:`_sync_groups_from_provider`. Omitting it disables the sync for
        the request rather than falling back to a claim.
        """
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

                # koalixcrm#430: the tenant alias must derive from the
                # VALIDATED token's issuer, never from claim content. The
                # caller tells us which issuer it validated against;
                # cross-checking the token's own `iss` against it keeps that
                # property true *for this request* rather than true only by
                # construction. A mismatch — or a claim set that never carried
                # `iss` — degrades the same way an unregistered OidcTenant
                # does: skip the sync, log it, never block authentication.
                token_issuer = user_info.get('iss')
                if not validated_issuer or token_issuer != validated_issuer:
                    logger.info(
                        "Token issuer %r does not match the issuer this "
                        "request was validated against (%r), or was not "
                        "present in the claims — skipping group sync for "
                        "user %s.",
                        token_issuer, validated_issuer, user.email,
                    )
                else:
                    _sync_groups_from_provider(user, user_info, issuer=validated_issuer)

            return user
        except Exception as e:
            logger.error(f"Authentication error for {provider} user {user_email}: {e}", exc_info=True)
            return None

    def _authenticate_with_id_token(self, id_token: str, **kwargs: Any) -> AbstractBaseUser | None:
        """Legacy authentication path using JWT validation."""
        access_token = kwargs.get('access_token')

        try:
            from django.conf import settings
            issuer = getattr(settings, 'OIDC_ISSUER', None)
            if not issuer:
                return None

            payload = validate_jwt(id_token, authority_url=issuer, access_token=access_token)

            user_info = {
                # `iss` is carried through so the group sync can resolve the
                # OidcTenant from the validated issuer (koalixcrm#430).
                'iss': payload.get('iss'),
                'email': payload.get('email'),
                'given_name': payload.get('given_name', ''),
                'family_name': payload.get('family_name', ''),
                'cognito:groups': payload.get('cognito:groups', []),
                'groups': payload.get('groups', []),
                'realm_access': payload.get('realm_access', {}),
            }

            return self._authenticate_with_user_info('oidc', user_info, validated_issuer=issuer)
        except Exception as e:
            logger.error(f"OIDC Authentication Error: {e}", exc_info=True)
            return None

    @staticmethod
    def _find_or_create_user(email: str, user_info: dict[str, Any]) -> AbstractBaseUser | None:
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

    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
