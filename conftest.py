# -*- coding: utf-8 -*-
"""
Root conftest.py — shared fixtures for all koalixcrm tests.

Authentication strategy:
- Unit tests (no external services): use BasicAuth via superuser
- Integration tests (cloud Keycloak available): use M2M access tokens
  when CELERY_WORKER_M2M_OIDC_ISSUER is set, otherwise fall back to BasicAuth
"""
import os
import pytest


@pytest.fixture
def admin_user(db):
    """Create a Django superuser for test authentication.

    Django is imported lazily so this conftest stays importable under the
    `unit-celery` profile (which runs with `-p no:django` and no configured
    DJANGO_SETTINGS_MODULE).
    """
    from django.contrib.auth.models import User

    user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if not user.check_password('adminpassword'):
        user.set_password('adminpassword')
        user.save()
    return user


@pytest.fixture
def use_m2m_auth():
    """Returns True if M2M OIDC environment is configured (integration tests)."""
    return bool(os.environ.get('CELERY_WORKER_M2M_OIDC_ISSUER'))
