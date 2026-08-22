# -*- coding: utf-8 -*-
"""koalixcrm#430 — a claim value can no longer name a locally meaningful group.

The defect these cover: ``_sync_groups_from_provider`` used to turn every
claim value into a Django group verbatim via ``get_or_create``, so an IdP
emitting a claim whose value equalled ``settings.M2M_MICROSERVICE_GROUP_NAME``
both created that group and put the bearer in it.

The fix is namespacing by *construction* — ``oidc:<tenantAlias>:<claimValue>``
with the alias resolved from a registered ``core.OidcTenant`` — so the
collision is not detected, it is unrepresentable.
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from koalixcrm.auth.oidc_backend import _sync_groups_from_provider
from koalixcrm.core.models.oidc_tenant import OidcTenant

User = get_user_model()

ISSUER = 'https://auth.example.test/realms/tenant-one'


@pytest.fixture
def user(db):
    return User.objects.create_user(username='claimant', email='claimant@example.test', password='pw')


@pytest.fixture
def tenant(db):
    return OidcTenant.objects.create(alias='tenant-one', issuer=ISSUER, display_name='Tenant One')


@pytest.mark.django_db
class TestGroupNamespacing:
    def test_claim_value_is_namespaced(self, user, tenant):
        _sync_groups_from_provider(user, {'groups': ['engineering']}, issuer=ISSUER)
        assert set(user.groups.values_list('name', flat=True)) == {'oidc:tenant-one:engineering'}

    def test_claim_cannot_name_the_service_account_group(self, user, tenant, settings):
        """The exploitable composition from the issue, now inert."""
        from koalixcrm.core.access import is_unrestricted_actor

        settings.M2M_MICROSERVICE_GROUP_NAME = 'koalixcrm-microservices'
        _sync_groups_from_provider(
            user, {'groups': ['koalixcrm-microservices']}, issuer=ISSUER
        )

        assert not Group.objects.filter(name='koalixcrm-microservices').exists()
        assert set(user.groups.values_list('name', flat=True)) == {
            'oidc:tenant-one:koalixcrm-microservices'
        }
        assert is_unrestricted_actor(user) is False

    def test_claim_cannot_forge_another_tenants_namespace(self, user, tenant):
        """A claim that *looks* namespaced is still namespaced under its own tenant."""
        _sync_groups_from_provider(
            user, {'groups': ['oidc:other-tenant:admins']}, issuer=ISSUER
        )
        assert set(user.groups.values_list('name', flat=True)) == {
            'oidc:tenant-one:oidc:other-tenant:admins'
        }
        assert not Group.objects.filter(name='oidc:other-tenant:admins').exists()

    def test_existing_django_groups_are_never_removed(self, user, tenant):
        local = Group.objects.create(name='locally-administered')
        user.groups.add(local)
        _sync_groups_from_provider(user, {'groups': ['engineering']}, issuer=ISSUER)
        assert set(user.groups.values_list('name', flat=True)) == {
            'locally-administered', 'oidc:tenant-one:engineering',
        }

    def test_realm_access_roles_are_namespaced_too(self, user, tenant):
        _sync_groups_from_provider(
            user, {'realm_access': {'roles': ['offline_access']}}, issuer=ISSUER
        )
        assert set(user.groups.values_list('name', flat=True)) == {
            'oidc:tenant-one:offline_access'
        }


@pytest.mark.django_db
class TestFailClosed:
    def test_unregistered_issuer_syncs_nothing(self, user):
        """No OidcTenant row → skip entirely: no group, no membership, no raise."""
        _sync_groups_from_provider(user, {'groups': ['engineering']}, issuer=ISSUER)
        assert user.groups.count() == 0
        assert Group.objects.count() == 0

    def test_absent_issuer_syncs_nothing(self, user, tenant):
        """A registered tenant does not help if the request has no validated issuer."""
        _sync_groups_from_provider(user, {'groups': ['engineering']}, issuer=None)
        assert user.groups.count() == 0

    def test_a_different_issuer_does_not_borrow_the_alias(self, user, tenant):
        _sync_groups_from_provider(
            user, {'groups': ['engineering']}, issuer='https://evil.example.test/realms/x'
        )
        assert user.groups.count() == 0

    def test_registering_the_tenant_is_the_opt_in(self, user):
        _sync_groups_from_provider(user, {'groups': ['engineering']}, issuer=ISSUER)
        assert user.groups.count() == 0

        OidcTenant.objects.create(alias='tenant-one', issuer=ISSUER)
        _sync_groups_from_provider(user, {'groups': ['engineering']}, issuer=ISSUER)
        assert set(user.groups.values_list('name', flat=True)) == {'oidc:tenant-one:engineering'}


@pytest.mark.django_db
class TestIssuerCrossCheck:
    """The alias must derive from the *validated* issuer, never from claims."""

    def _backend(self):
        from koalixcrm.auth.oidc_backend import OIDCAuthenticationBackend
        return OIDCAuthenticationBackend()

    def test_mismatched_iss_claim_skips_the_sync(self, tenant, settings):
        settings.ADMIN_OIDC_ISSUER = ISSUER
        info = {
            'iss': 'https://evil.example.test/realms/x',
            'email': 'x@example.test',
            'groups': ['engineering'],
        }
        user = self._backend()._authenticate_with_user_info(
            'oidc', info, validated_issuer=ISSUER
        )
        assert user is not None
        assert user.groups.count() == 0

    def test_matching_iss_claim_syncs(self, tenant, settings):
        settings.ADMIN_OIDC_ISSUER = ISSUER
        info = {'iss': ISSUER, 'email': 'y@example.test', 'groups': ['engineering']}
        user = self._backend()._authenticate_with_user_info(
            'oidc', info, validated_issuer=ISSUER
        )
        assert set(user.groups.values_list('name', flat=True)) == {'oidc:tenant-one:engineering'}

    def test_no_validated_issuer_skips_the_sync(self, tenant):
        info = {'iss': ISSUER, 'email': 'z@example.test', 'groups': ['engineering']}
        user = self._backend()._authenticate_with_user_info('oidc', info, validated_issuer=None)
        assert user is not None
        assert user.groups.count() == 0
