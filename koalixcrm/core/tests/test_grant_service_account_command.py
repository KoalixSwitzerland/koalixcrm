# -*- coding: utf-8 -*-
"""koalixcrm#432 — the administrative write path for ServiceAccountGrant.

The command exists so that granting unrestricted-actor status has exactly two
entry points, both administrative: the superuser-only admin and this command.
Nothing in an authentication or synchronisation path may create a grant.
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from koalixcrm.core.models.service_account_grant import ServiceAccountGrant

User = get_user_model()


@pytest.fixture
def svc(db):
    return User.objects.create_user(username='svc-worker', password='pw')


@pytest.mark.django_db
class TestGrantServiceAccountCommand:
    def test_grants_named_user(self, svc):
        call_command('grant_service_account', 'svc-worker')
        assert ServiceAccountGrant.objects.filter(user=svc).exists()

    def test_is_idempotent(self, svc):
        call_command('grant_service_account', 'svc-worker')
        call_command('grant_service_account', 'svc-worker')
        assert ServiceAccountGrant.objects.filter(user=svc).count() == 1

    def test_defaults_to_the_m2m_client_id(self, svc, settings):
        settings.CELERY_WORKER_M2M_CLIENT_ID = 'svc-worker'
        call_command('grant_service_account')
        assert ServiceAccountGrant.objects.filter(user=svc).exists()

    def test_revoke_removes_the_grant(self, svc):
        ServiceAccountGrant.objects.create(user=svc)
        call_command('grant_service_account', 'svc-worker', '--revoke')
        assert not ServiceAccountGrant.objects.filter(user=svc).exists()

    def test_unknown_user_is_an_error_not_a_new_identity(self, db):
        """The command grants authority; it does not mint users."""
        with pytest.raises(CommandError):
            call_command('grant_service_account', 'nobody-here')
        assert not User.objects.filter(username='nobody-here').exists()

    def test_no_username_and_no_setting_is_an_error(self, db, settings):
        settings.CELERY_WORKER_M2M_CLIENT_ID = ''
        with pytest.raises(CommandError):
            call_command('grant_service_account')
