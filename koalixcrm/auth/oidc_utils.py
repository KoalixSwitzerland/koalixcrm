import base64
import hashlib
import json
import logging
from urllib.request import urlopen

import jwt
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

JWKS_CACHE_TIMEOUT = 60 * 60
OIDC_DISCOVERY_CACHE_TIMEOUT = 60 * 60


def get_oidc_discovery(issuer_url):
    """Fetch and cache the OIDC discovery document."""
    if not issuer_url:
        logger.error("get_oidc_discovery called without issuer_url")
        return None

    cache_key = f"oidc_discovery_{hash(issuer_url)}"
    config = cache.get(cache_key)
    if config:
        return config

    well_known_url = f"{issuer_url.rstrip('/')}/.well-known/openid-configuration"
    try:
        with urlopen(well_known_url) as resp:
            config = json.loads(resp.read())
            cache.set(cache_key, config, OIDC_DISCOVERY_CACHE_TIMEOUT)
            logger.info(f"Successfully fetched OIDC discovery from {well_known_url}")
            return config
    except Exception as e:
        logger.error(f"Error fetching OIDC discovery from {well_known_url}: {e}", exc_info=True)
        return None


def get_jwks(authority_url):
    """Get the JSON Web Key Set from the OIDC provider, with caching."""
    if not authority_url:
        logger.error("get_jwks called without authority_url")
        return None

    cache_key = f"oidc_jwks_{hash(authority_url)}"
    jwks = cache.get(cache_key)
    if jwks:
        return jwks

    discovery = get_oidc_discovery(authority_url)
    if discovery and discovery.get('jwks_uri'):
        jwks_url = discovery['jwks_uri']
    else:
        jwks_url = f"{authority_url.rstrip('/')}/.well-known/jwks.json"
        logger.warning(f"OIDC discovery failed for {authority_url}, falling back to {jwks_url}")

    try:
        with urlopen(jwks_url) as jsonurl:
            jwks = json.loads(jsonurl.read())
            cache.set(cache_key, jwks, JWKS_CACHE_TIMEOUT)
            logger.info(f"Successfully fetched JWKS from {jwks_url}")
            return jwks
    except Exception as e:
        logger.error(f"Error fetching JWKS from {jwks_url}: {e}", exc_info=True)
        return None


def validate_jwt(token, authority_url, access_token=None, client_id=None):
    """Validate a JWT token against an OIDC provider."""
    if not authority_url:
        raise AuthenticationFailed('OIDC issuer URL is required for JWT validation.')

    jwks = get_jwks(authority_url)
    if not jwks:
        raise AuthenticationFailed('Could not retrieve signing keys from provider.')

    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.PyJWTError:
        raise AuthenticationFailed('Invalid token header.')

    if 'kid' not in unverified_header:
        raise AuthenticationFailed('Invalid token header: No KID')

    rsa_key = None
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"], "kid": key["kid"], "use": key["use"],
                "n": key["n"], "e": key["e"]
            }
            break

    if not rsa_key:
        raise AuthenticationFailed('Unable to find appropriate key in JWKS.')

    try:
        signing_key = jwt.PyJWK(rsa_key).key
        decode_kwargs = {
            "algorithms": ["RS256"],
            "issuer": authority_url,
        }

        if client_id is not None:
            decode_kwargs["audience"] = client_id
        else:
            decode_kwargs["options"] = {"verify_aud": False}

        payload = jwt.decode(token, signing_key, **decode_kwargs)

        if access_token and payload.get('at_hash'):
            _verify_at_hash(payload['at_hash'], access_token)

        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired.')
    except jwt.InvalidTokenError as e:
        logger.debug(f"JWT Claims Error: {e}")
        raise AuthenticationFailed(f'Invalid claims: {e}')
    except Exception as e:
        raise AuthenticationFailed(f'Unable to parse authentication token: {str(e)}')


def _verify_at_hash(at_hash, access_token):
    """Verify the at_hash claim in an ID token matches the access token."""
    digest = hashlib.sha256(access_token.encode('ascii')).digest()
    expected = base64.urlsafe_b64encode(digest[:16]).rstrip(b'=').decode('ascii')
    if at_hash != expected:
        raise jwt.InvalidTokenError('at_hash mismatch')


def get_token_auth_header(request):
    """Get the Access Token from the Authorization Header."""
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    parts = auth.split()
    if not parts or parts[0].lower() != "bearer" or len(parts) != 2:
        return None
    return parts[1]
