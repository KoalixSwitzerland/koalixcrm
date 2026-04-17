import logging
import urllib.parse

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

logger = logging.getLogger(__name__)

SUPPORTED_PROVIDERS = ['oidc']

# Register OAuth providers
oauth = OAuth()

if getattr(settings, 'ADMIN_OIDC_ISSUER', None):
    oauth.register(
        name='oidc',
        server_metadata_url=f'{settings.ADMIN_OIDC_ISSUER.rstrip("/")}/.well-known/openid-configuration',
        client_id=settings.ADMIN_OIDC_CLIENT_ID,
        client_secret=getattr(settings, 'ADMIN_OIDC_CLIENT_SECRET', None),
        client_kwargs={
            'scope': 'openid profile email',
            'code_challenge_method': 'S256',
            'token_endpoint_auth_method': 'client_secret_post',
        },
    )


def _build_absolute_url(request, path):
    """Build an absolute URL using SITE_URL if available, otherwise from the request."""
    site_url = getattr(settings, 'SITE_URL', '')
    if site_url:
        return f"{site_url.rstrip('/')}{path}"
    return request.build_absolute_uri(path)


class LoginSelectionView(View):
    """
    Admin login view. Redirects directly to OIDC provider OAuth flow.
    """
    def get(self, request):
        next_url = request.GET.get('next', '')

        if request.user.is_authenticated:
            if next_url:
                return redirect(next_url)
            if request.user.is_staff:
                return redirect('admin:index')
            return redirect('/')

        oidc_url = reverse('oauth-login', kwargs={'provider': 'oidc'})
        if next_url:
            oidc_url += f'?next={next_url}'
        return redirect(oidc_url)


class OAuthLoginView(View):
    """
    Initiates the OAuth flow for a specific provider.
    """
    def get(self, request, provider):
        if provider not in SUPPORTED_PROVIDERS:
            return HttpResponse(f'Unsupported provider: {provider}', status=400)

        if request.user.is_authenticated:
            next_url = request.GET.get('next', '/admin/')
            return redirect(next_url)

        next_url = request.GET.get('next', '')
        if next_url:
            request.session['login_next_url'] = next_url

        callback_path = reverse('oauth-callback', kwargs={'provider': provider})
        redirect_uri = _build_absolute_url(request, callback_path)
        logger.info(f"OAuth redirect_uri: {redirect_uri}")

        try:
            oauth_client = getattr(oauth, provider)
        except AttributeError:
            logger.error(f"OAuth provider '{provider}' is not registered.")
            return HttpResponse(
                f'OAuth provider "{provider}" is not configured.',
                status=500
            )

        return oauth_client.authorize_redirect(request, redirect_uri)


class OAuthCallbackView(View):
    """
    Handles the OAuth callback. Exchanges authorization code for tokens,
    creates/links the user, and redirects to the admin.
    """
    def get(self, request, provider):
        if provider not in SUPPORTED_PROVIDERS:
            return HttpResponse(f'Unsupported provider: {provider}', status=400)

        try:
            oauth_client = getattr(oauth, provider)
            token_data = oauth_client.authorize_access_token(request)

            user_info = self._extract_user_info(provider, token_data)

            if not user_info or not user_info.get('email'):
                logger.error(f"Failed to extract user info from {provider}")
                return HttpResponse('Authentication failed: no user info.', status=401)

            user = authenticate(request=request, provider=provider, user_info=user_info)

            if user is None:
                logger.error(f"authenticate() returned None for {user_info.get('email')}")
                return HttpResponse('Authentication failed.', status=401)

            if not user.is_active:
                return HttpResponse('User account is not active.', status=403)

            login(request, user)

            request.session['auth_provider'] = provider
            request.session['user_email'] = user.email

            next_url = request.session.pop('login_next_url', None)

            if next_url and '/admin' in next_url and not user.is_staff:
                logout(request)
                return HttpResponse('Access denied: Admin privileges required.', status=403)

            if next_url:
                return redirect(next_url)

            if user.is_staff:
                return redirect('admin:index')

            return redirect('/')

        except Exception as e:
            logger.error(f"OAuth callback error: {type(e).__name__}: {e}", exc_info=True)
            return HttpResponse(f"Authentication error: {type(e).__name__}: {e}", status=500)

    def _extract_user_info(self, provider, token_data):
        """Extract user info from OIDC token data."""
        try:
            userinfo = token_data.get('userinfo')
            if userinfo and userinfo.get('email'):
                return self._normalize_claims(userinfo)

            try:
                oauth_client = getattr(oauth, provider)
                userinfo = oauth_client.userinfo(token=token_data)
                if userinfo and userinfo.get('email'):
                    return self._normalize_claims(userinfo)
            except Exception as e:
                logger.warning(f"Userinfo endpoint call failed: {e}")

            id_token = token_data.get('id_token')
            if id_token:
                import json
                import base64
                payload_b64 = id_token.split('.')[1]
                payload_b64 += '=' * (4 - len(payload_b64) % 4)
                claims = json.loads(base64.urlsafe_b64decode(payload_b64))
                if claims.get('email'):
                    return self._normalize_claims(claims)

        except Exception as e:
            logger.error(f"Error extracting user info: {e}", exc_info=True)
        return None

    def _normalize_claims(self, claims):
        return {
            'sub': claims.get('sub'),
            'email': claims.get('email'),
            'given_name': claims.get('given_name', ''),
            'family_name': claims.get('family_name', ''),
            'cognito:groups': claims.get('cognito:groups', []),
            'groups': claims.get('groups', []),
            'realm_access': claims.get('realm_access', {}),
        }


class MultiProviderLogoutView(LogoutView):
    """
    Logout with federated OIDC end_session_endpoint support.
    """
    def dispatch(self, request, *args, **kwargs):
        logout(request)

        next_url = request.GET.get('next', '')
        if next_url:
            post_logout_uri = _build_absolute_url(request, next_url)
        else:
            login_url = reverse('login-selection')
            post_logout_uri = _build_absolute_url(request, login_url)

        client_id = getattr(settings, 'ADMIN_OIDC_CLIENT_ID', '')

        issuer = getattr(settings, 'ADMIN_OIDC_ISSUER', None)
        if issuer:
            try:
                from .oidc_utils import get_oidc_discovery
                config = get_oidc_discovery(issuer)
                end_session_endpoint = config.get('end_session_endpoint') if config else None
                if end_session_endpoint:
                    params = {'post_logout_redirect_uri': post_logout_uri}
                    if client_id:
                        params['client_id'] = client_id
                    url = f'{end_session_endpoint}?{urllib.parse.urlencode(params)}'
                    return redirect(url)
            except Exception as e:
                logger.warning(f"Failed to discover end_session_endpoint: {e}")

        return redirect('login-selection')
