# -*- coding: utf-8 -*-
"""koalixcrm#443 -- open redirect through the ``next`` parameter of the OIDC views.

Only same-host URLs may be honoured; everything else must fall back to the
view's existing default. ``oauth.oidc`` only exists when ``ADMIN_OIDC_ISSUER``
is set at import time, so the module-level ``oauth`` object is patched.
"""
from unittest import mock
from urllib.parse import parse_qs, urlparse

import pytest
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

User = get_user_model()

EVIL = 'https://evil.example/'
MALFORMED_NEXT = ['foo', 'admin:index', '@evil.example', '/admin/\nfoo', '/admin/\rfoo']
VIEWS = 'koalixcrm.auth.oidc_views'


def _location(response):
    return response['Location']


def _leaves_site(location):
    """True if following ``location`` from the test server would leave it."""
    parsed = urlparse(location)
    return bool(parsed.netloc) and parsed.netloc != 'testserver'


@pytest.fixture
def staff(db):
    return User.objects.create_user(
        username='staffer', email='staffer@example.test', password='pw', is_staff=True
    )


@pytest.fixture
def plain(db):
    return User.objects.create_user(username='plain', email='plain@example.test', password='pw')


@pytest.fixture
def fake_oauth():
    """A stand-in for ``oidc_views.oauth`` with a registered ``oidc`` client."""
    oauth = mock.MagicMock()
    oauth.oidc.authorize_redirect.side_effect = (
        lambda request, redirect_uri: HttpResponseRedirect('https://idp.example.test/authorize')
    )
    with mock.patch(f'{VIEWS}.oauth', oauth):
        yield oauth


# --- 1. LoginSelectionView, authenticated ---------------------------------

@pytest.mark.django_db
class TestLoginSelectionAuthenticated:
    @pytest.mark.parametrize('evil_next', [
        EVIL, '//evil.example/', 'https:evil.example', '/\\evil.example', 'javascript:alert(1)',
    ])
    def test_external_next_is_ignored_for_staff(self, client, staff, evil_next):
        client.force_login(staff)
        response = client.get(reverse('login-selection'), {'next': evil_next})
        assert response.status_code == 302
        assert _location(response) == reverse('admin:index')

    @pytest.mark.parametrize('bad_next', MALFORMED_NEXT)
    def test_malformed_next_falls_back_to_default(self, client, staff, bad_next):
        client.force_login(staff)
        response = client.get(reverse('login-selection'), {'next': bad_next})
        assert response.status_code == 302
        assert _location(response) == reverse('admin:index')

    def test_external_next_is_ignored_for_non_staff(self, client, plain):
        client.force_login(plain)
        response = client.get(reverse('login-selection'), {'next': EVIL})
        assert _location(response) == '/'

    def test_local_next_still_honoured(self, client, staff):
        client.force_login(staff)
        response = client.get(reverse('login-selection'), {'next': '/admin/crm/task/'})
        assert _location(response) == '/admin/crm/task/'

    def test_same_host_absolute_next_still_honoured(self, client, staff):
        client.force_login(staff)
        response = client.get(reverse('login-selection'), {'next': 'http://testserver/admin/crm/task/'})
        assert _location(response) == 'http://testserver/admin/crm/task/'


# --- 2. LoginSelectionView, unauthenticated, OIDC configured --------------

@pytest.mark.django_db
class TestLoginSelectionUnauthenticated:
    def test_next_is_urlencoded_into_oauth_login_url(self, client, fake_oauth):
        response = client.get(reverse('login-selection'), {'next': '/a&foo=b'})
        query = parse_qs(urlparse(_location(response)).query)
        assert query == {'next': ['/a&foo=b']}, 'next must be one encoded parameter, no injected foo'

    def test_external_next_is_not_forwarded(self, client, fake_oauth):
        response = client.get(reverse('login-selection'), {'next': EVIL})
        assert 'evil.example' not in _location(response)

    def test_local_next_still_forwarded(self, client, fake_oauth):
        response = client.get(reverse('login-selection'), {'next': '/admin/crm/task/'})
        oauth_login = reverse('oauth-login', kwargs={'provider': 'oidc'})
        parsed = urlparse(_location(response))
        assert parsed.path == oauth_login
        assert parse_qs(parsed.query) == {'next': ['/admin/crm/task/']}


# --- 3./4. OAuthLoginView --------------------------------------------------

@pytest.mark.django_db
class TestOAuthLogin:
    URL = '/auth/login/oidc/'

    def test_authenticated_external_next_is_ignored(self, client, staff, fake_oauth):
        client.force_login(staff)
        response = client.get(reverse('oauth-login', kwargs={'provider': 'oidc'}), {'next': EVIL})
        assert response.status_code == 302
        assert not _leaves_site(_location(response))
        assert _location(response) == '/admin/'

    def test_authenticated_local_next_still_honoured(self, client, staff, fake_oauth):
        client.force_login(staff)
        response = client.get(
            reverse('oauth-login', kwargs={'provider': 'oidc'}), {'next': '/admin/crm/task/'}
        )
        assert _location(response) == '/admin/crm/task/'

    @pytest.mark.parametrize('evil_next', [EVIL, '//evil.example/', 'javascript:alert(1)'])
    def test_unauthenticated_external_next_not_stored_in_session(self, client, fake_oauth, evil_next):
        client.get(reverse('oauth-login', kwargs={'provider': 'oidc'}), {'next': evil_next})
        assert 'evil.example' not in client.session.get('login_next_url', '')
        assert 'javascript' not in client.session.get('login_next_url', '')

    def test_unauthenticated_local_next_stored_in_session(self, client, fake_oauth):
        client.get(reverse('oauth-login', kwargs={'provider': 'oidc'}), {'next': '/admin/crm/task/'})
        assert client.session['login_next_url'] == '/admin/crm/task/'


# --- 5. OAuthCallbackView --------------------------------------------------

@pytest.mark.django_db
class TestOAuthCallback:
    def _callback(self, client, user, fake_oauth, next_url):
        fake_oauth.oidc.authorize_access_token.return_value = {
            'userinfo': {'sub': 's1', 'iss': 'https://idp.example.test', 'email': user.email}
        }
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        session = client.session
        session['login_next_url'] = next_url
        session.save()
        with mock.patch(f'{VIEWS}.authenticate', return_value=user):
            return client.get(reverse('oauth-callback', kwargs={'provider': 'oidc'}))

    @pytest.mark.parametrize('evil_next', [EVIL, '//evil.example/'])
    def test_external_session_next_is_ignored_for_staff(self, client, staff, fake_oauth, evil_next):
        response = self._callback(client, staff, fake_oauth, evil_next)
        assert response.status_code == 302
        assert _location(response) == reverse('admin:index')

    @pytest.mark.parametrize('bad_next', MALFORMED_NEXT)
    def test_malformed_session_next_falls_back_to_default(self, client, staff, fake_oauth, bad_next):
        response = self._callback(client, staff, fake_oauth, bad_next)
        assert response.status_code == 302
        assert _location(response) == reverse('admin:index')

    def test_external_session_next_is_ignored_for_non_staff(self, client, plain, fake_oauth):
        response = self._callback(client, plain, fake_oauth, EVIL)
        assert response.status_code == 302
        assert _location(response) == '/'

    def test_local_next_still_honoured(self, client, staff, fake_oauth):
        response = self._callback(client, staff, fake_oauth, '/admin/crm/task/')
        assert _location(response) == '/admin/crm/task/'

    def test_admin_next_still_denied_for_non_staff(self, client, plain, fake_oauth):
        response = self._callback(client, plain, fake_oauth, '/admin/crm/task/')
        assert response.status_code == 403


# --- 6. MultiProviderLogoutView -------------------------------------------

@pytest.mark.django_db
class TestLogoutPostLogoutRedirect:
    SITE = 'https://crm.example.test'

    def _post_logout_uri(self, client, settings, next_url, site_url=SITE):
        settings.ADMIN_OIDC_ISSUER = 'https://idp.example.test/realms/x'
        settings.SITE_URL = site_url
        discovery = {'end_session_endpoint': 'https://idp.example.test/logout'}
        with mock.patch('koalixcrm.auth.oidc_utils.get_oidc_discovery', return_value=discovery):
            response = client.get(reverse('logout'), {'next': next_url})
        assert response.status_code == 302
        assert _location(response).startswith('https://idp.example.test/logout?')
        return parse_qs(urlparse(_location(response)).query)['post_logout_redirect_uri'][0]

    def test_at_sign_next_cannot_change_host(self, client, settings):
        uri = self._post_logout_uri(client, settings, '@evil.example')
        assert urlparse(uri).hostname == 'crm.example.test'

    def test_absolute_external_next_cannot_change_host_without_site_url(self, client, settings):
        uri = self._post_logout_uri(client, settings, EVIL, site_url='')
        assert urlparse(uri).hostname != 'evil.example'

    def test_external_next_falls_back_to_login_page(self, client, settings):
        uri = self._post_logout_uri(client, settings, EVIL)
        assert uri == f'{self.SITE}{reverse("login-selection")}'

    def test_local_next_still_honoured(self, client, settings):
        uri = self._post_logout_uri(client, settings, '/admin/crm/task/')
        assert uri == f'{self.SITE}/admin/crm/task/'
