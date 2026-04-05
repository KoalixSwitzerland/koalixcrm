# -*- coding: utf-8 -*-
"""
BaseAPIClient - Shared base class for all koalixcrm API clients.
Ported from qq_workflow_support_webapp_backend.

Provides:
- OIDC M2M token discovery + client credentials flow
- Basic Auth session login (for testing with LiveServerTestCase)
- HTTP/HTTPS request execution with retry on 401/403
- Custom origin verification header support
- Object caching, pagination, and CRUD helpers
"""
import base64
import http.client
import json
import logging
import socket
import urllib.parse
from os import getenv
from typing import Any, Dict, List, Optional, Type

from koalixcrm.shared.token_cache import TokenCache
from koalixcrm.shared.object_cache import ObjectCache, T

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """
    Base API client with shared authentication, request execution,
    object caching, pagination, and CRUD helpers.

    Subclasses must set:
        - api_path_env_var: str  -- env var name for the API path
        - api_path_default: str  -- default value for the API path

    Subclasses may set:
        - uses_workspace_id: bool  -- whether workspace_id is part of the URL path (default False)
        - uses_object_cache: bool  -- whether to initialise an ObjectCache (default True)
    """

    # Subclass configuration
    api_path_env_var: str = ''
    api_path_default: str = ''
    uses_workspace_id: bool = False
    uses_object_cache: bool = True

    def __init__(self, api_url: str = None, username: str = None, password: str = None, workspace_id: int = None):
        # Store authentication method
        self.username = username
        self.password = password
        self.use_session_auth = username is not None and password is not None

        # Get M2M client configuration from environment variables
        self.client_id = getenv('CELERY_WORKER_M2M_CLIENT_ID')
        self.client_secret = getenv('CELERY_WORKER_M2M_CLIENT_SECRET')
        self.m2m_oidc_issuer = getenv('CELERY_WORKER_M2M_OIDC_ISSUER')
        self.api = api_url or getenv('KOALIXCRM_API_URL')
        self.workspace_id = workspace_id if self.uses_workspace_id else None
        self.agent_application_path = getenv(self.api_path_env_var, self.api_path_default)
        self.scope = getenv('CELERY_WORKER_M2M_SCOPE')

        # Custom origin header validation configuration
        self.custom_origin_verification_enabled = getenv('X_CUSTOM_ORIGIN_VERIFICATION_ON', 'false').lower() == 'true'
        self.custom_origin_verification_key = getenv('X_CUSTOM_ORIGIN_VERIFICATION_KEY', '')

        # Initialize token cache
        self._token_cache = TokenCache()

        # Get a token (this will check the cache first) - only for M2M auth
        if not self.use_session_auth:
            self.token, self.token_type = self.get_token()
        else:
            self.token = None
            self.token_type = None
            self._session_token = None
            self._login_with_session()

        # Initialize object cache (None when disabled so helpers fail with a clear message)
        self._cache = ObjectCache() if self.uses_object_cache else None

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def _login_with_session(self):
        """
        Login to Django using Basic Authentication (username/password).
        For testing with LiveServerTestCase, we use HTTP Basic Auth which Django REST framework supports.
        """
        if not self.username or not self.password:
            raise ValueError("Username and password are required for session authentication")

        credentials = f"{self.username}:{self.password}"
        self._session_token = base64.b64encode(credentials.encode()).decode('ascii')

    def _discover_token_endpoint(self) -> str:
        """Discover the token endpoint URL from OIDC well-known configuration."""
        if not self.m2m_oidc_issuer:
            raise ValueError(
                "CELERY_WORKER_M2M_OIDC_ISSUER is not set. "
                "Set this environment variable to enable M2M authentication."
            )

        well_known_url = f"{self.m2m_oidc_issuer.rstrip('/')}/.well-known/openid-configuration"
        try:
            parsed = urllib.parse.urlparse(well_known_url)
            conn = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=10)
            conn.request("GET", parsed.path)
            res = conn.getresponse()
            if res.status == 200:
                config = json.loads(res.read().decode("utf-8"))
                token_endpoint = config.get('token_endpoint')
                if token_endpoint:
                    return token_endpoint
            raise ValueError(f"OIDC discovery returned status {res.status}")
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(
                f"Failed to discover token endpoint from {well_known_url}: {e}"
            ) from e

    def get_token(self) -> tuple:
        """
        Get an access token using client credentials flow.
        First checks the cache, and if no valid token is found, gets a new one.

        Returns:
            tuple: (access_token, token_type)
        """
        cached_token = self._token_cache.get_token()
        if cached_token:
            return cached_token

        token_url = self._discover_token_endpoint()

        if not token_url.startswith(('http://', 'https://')):
            raise ValueError(
                f"Token endpoint URL must start with http:// or https://. "
                f"Current value: '{token_url}'"
            )

        parsed_url = urllib.parse.urlparse(token_url)
        host = parsed_url.hostname
        if not host:
            raise ValueError(
                f"Failed to parse hostname from token endpoint URL: '{token_url}'"
            )

        port = parsed_url.port or 443
        token_path = parsed_url.path or '/oauth2/token'

        try:
            conn = http.client.HTTPSConnection(host, port, timeout=10)
        except Exception as e:
            raise ValueError(
                f"Failed to create HTTPS connection to '{host}:{port}': {e}. "
                f"Token endpoint URL: '{token_url}'"
            ) from e

        payload_dict = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
        }
        if self.scope:
            payload_dict['scope'] = self.scope
        payload = urllib.parse.urlencode(payload_dict)
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        try:
            conn.request("POST", token_path, payload, headers)
            res = conn.getresponse()
            data = res.read()
        except Exception as e:
            if isinstance(e, socket.gaierror):
                raise ValueError(
                    f"DNS resolution failed for hostname '{host}': {e}. "
                    f"Token endpoint URL: '{token_url}'"
                ) from e
            else:
                raise ValueError(
                    f"Failed to connect to '{host}:{port}': {e}. "
                    f"Token endpoint URL: '{token_url}'"
                ) from e

        if res.status == 200:
            decoded_data = data.decode("utf-8")
            decoded_data_dict = json.loads(decoded_data)
            token_type = decoded_data_dict.get('token_type', '').strip()
            access_token = decoded_data_dict.get('access_token', '').strip()
            identity_token = decoded_data_dict.get('id_token', '').strip()
            save_to_env = getenv('KOALIXCRM_TOKEN_SAVE_TO_ENV', 'false').lower() == 'true'
            self._token_cache.set_token(access_token, token_type, identity_token, save_to_env=save_to_env)
            return access_token, token_type
        else:
            logger.error("Error getting token: %s %s", res.status, res.reason)
            logger.error(data.decode("utf-8"))
            raise Exception(f"Failed to get token: {res.status}")

    # ------------------------------------------------------------------
    # Request execution
    # ------------------------------------------------------------------

    def _make_request(self, endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Any:
        """Make a request to the API and return the response data."""
        return self._execute_request(endpoint, method, data)

    def _build_connection(self):
        """Parse the API URL and return (connection, host, port)."""
        if not self.api:
            raise ValueError("KOALIXCRM_API_URL environment variable is not set")

        parsed_url = urllib.parse.urlparse(self.api)
        host = parsed_url.hostname

        if not host:
            raise ValueError(
                f"Failed to parse hostname from KOALIXCRM_API_URL. "
                f"Current value: '{self.api}'. "
                f"Please ensure it's a valid URL (e.g., https://api.example.com)"
            )

        port = parsed_url.port
        is_https = parsed_url.scheme == 'https'

        if not port:
            port = 443 if is_https else 8000

        if is_https:
            conn = http.client.HTTPSConnection(host, port)
        else:
            conn = http.client.HTTPConnection(host, port)

        return conn, host, port

    def _build_headers(self) -> Dict[str, str]:
        """Build request headers based on the current authentication method."""
        if self.use_session_auth:
            headers = {'Content-Type': 'application/json'}
            if self._session_token:
                headers['Authorization'] = f'Basic {self._session_token}'
        else:
            token_type = (self.token_type or 'Bearer').strip()
            headers = {
                'Authorization': f"{token_type} {self.token}",
                'Content-Type': 'application/json',
            }

        if self.custom_origin_verification_enabled and self.custom_origin_verification_key:
            headers['X-Custom-Origin-Verify'] = self.custom_origin_verification_key

        return headers

    def _build_full_path(self, endpoint: str) -> str:
        """Build the full URL path including the app path and optional workspace_id."""
        app_path = self.agent_application_path
        if not app_path.endswith('/'):
            app_path += '/'

        clean_endpoint = endpoint.lstrip('/')

        if self.uses_workspace_id and self.workspace_id:
            return f"{app_path}{self.workspace_id}/{clean_endpoint}"
        return f"{app_path}{clean_endpoint}"

    def _handle_request_error(self, e: Exception, host: str, port: int,
                              method: str, full_path: str, endpoint: str,
                              data: Any) -> None:
        """Handle exceptions raised during request execution."""
        if isinstance(e, socket.gaierror):
            raise ValueError(
                f"DNS resolution failed for API hostname '{host}'. "
                f"Error: {str(e)}. "
                f"Current KOALIXCRM_API_URL: '{self.api}'\n"
                f"Parsed hostname: '{host}', port: {port}"
            ) from e
        elif isinstance(e, (ConnectionRefusedError, socket.error)) and "[Errno 111]" in str(e):
            logger.error(
                "CONNECTION REFUSED: Could not connect to %s. "
                "Request: %s %s. Possible causes: backend not running, "
                "Docker localhost mismatch, or wrong port.",
                self.api, method, full_path,
            )
        else:
            logger.error(
                "Request error: url=%s host=%s port=%s path=%s "
                "endpoint=%s method=%s data=%s — %s",
                self.api, host, port, self.agent_application_path,
                endpoint, method, data, e,
            )

    def _execute_request(self, endpoint: str, method: str = "GET",
                         data: Dict[str, Any] = None, retry: bool = True) -> Any:
        """Execute an API request with the current token or session."""
        # Ensure auth credentials are current
        if self.use_session_auth and not self._session_token:
            self._login_with_session()
        if not self.use_session_auth:
            cached_token = self._token_cache.get_token()
            if not cached_token:
                self.token, self.token_type = self.get_token()

        conn, host, port = self._build_connection()
        headers = self._build_headers()
        full_path = self._build_full_path(endpoint)

        try:
            if method == "GET":
                conn.request(method, full_path, headers=headers)
            else:
                payload = json.dumps(data) if data else None
                conn.request(method, full_path, payload, headers)

            res = conn.getresponse()
            response_data = res.read()

            if res.status in (200, 201):
                return json.loads(response_data.decode("utf-8"))

            if res.status in (401, 403) and retry:
                logger.warning(
                    "Authentication error (%s). Getting a new token and retrying...",
                    res.status,
                )
                if self.use_session_auth:
                    self._session_token = None
                    self._login_with_session()
                else:
                    self._token_cache.clear()
                    self.token, self.token_type = self.get_token()
                return self._execute_request(endpoint, method, data, retry=False)

            logger.error("Error making request to %s: %s %s", endpoint, res.status, res.reason)
            try:
                error_details = json.loads(response_data.decode("utf-8"))
                logger.error("Error details: %s", error_details)
            except json.JSONDecodeError:
                logger.error("Error body: %s", response_data.decode('utf-8'))
            return None
        except Exception as e:
            self._handle_request_error(e, host, port, method, full_path, endpoint, data)
            return None
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Object CRUD helpers
    # ------------------------------------------------------------------

    def _require_cache(self) -> ObjectCache:
        """Return the object cache or raise if it was not enabled."""
        if self._cache is None:
            raise RuntimeError(
                f"{self.__class__.__name__} has uses_object_cache=False. "
                f"Enable it or avoid calling CRUD helpers that require the cache."
            )
        return self._cache

    def _get_object(self, model_class: Type[T], endpoint: str, object_id: int) -> Optional[T]:
        """Get an object by its ID, using the cache if available."""
        cache = self._require_cache()
        cached_obj = cache.get(model_class, object_id)
        if cached_obj:
            return cached_obj

        data = self._make_request(f"{endpoint}/{object_id}/")
        if data:
            obj = model_class(data, self)
            cache.set(model_class, object_id, obj)
            return obj
        return None

    def _get_object_list(self, model_class: Type[T], endpoint: str) -> List[T]:
        """Get a list of objects from the API. Supports DRF pagination."""
        cache = self._require_cache()
        all_items: List[Dict[str, Any]] = []
        current_endpoint = endpoint

        while current_endpoint:
            data = self._make_request(current_endpoint)
            if not data:
                break

            if isinstance(data, dict) and isinstance(data.get("results"), list):
                all_items.extend(data.get("results", []))
                next_url = data.get("next")
                if next_url:
                    parsed_next = urllib.parse.urlparse(next_url)
                    current_endpoint = parsed_next.path
                    if parsed_next.query:
                        current_endpoint += f"?{parsed_next.query}"

                    app_path = self.agent_application_path
                    if not app_path.endswith('/'):
                        app_path += '/'

                    if self.uses_workspace_id and self.workspace_id:
                        prefix = f"{app_path}{self.workspace_id}/"
                    else:
                        prefix = app_path

                    if current_endpoint.startswith(prefix):
                        current_endpoint = current_endpoint[len(prefix):]
                else:
                    current_endpoint = None
            elif isinstance(data, list):
                all_items.extend(data)
                current_endpoint = None
            else:
                current_endpoint = None

        result: List[T] = []
        for item in all_items:
            if not isinstance(item, dict):
                continue
            object_id = item.get('id')
            obj = model_class(item, self)
            if object_id is not None:
                cache.set(model_class, object_id, obj)
            result.append(obj)
        return result

    def _put_full_update(self, model_class: Type[T], endpoint_base: str,
                         object_id: int, data: Dict[str, Any]) -> Optional[T]:
        """Perform a PUT update sending the full object payload merged with provided data."""
        cache = self._require_cache()
        existing = self._make_request(f"{endpoint_base}/{object_id}/")
        if not existing:
            return None
        payload = dict(existing)
        if data:
            payload.update(data)
        payload.pop('id', None)
        payload.pop('created_at', None)
        payload.pop('updated_at', None)

        flattened_payload = {}
        for key, value in payload.items():
            if isinstance(value, dict) and 'id' in value:
                flattened_payload[key] = value['id']
            else:
                flattened_payload[key] = value

        response_data = self._make_request(
            f"{endpoint_base}/{object_id}/", method="PUT", data=flattened_payload
        )
        if response_data:
            obj = model_class(response_data, self)
            cache.set(model_class, obj.id, obj)
            return obj
        return None

    def _patch_partial_update(self, model_class: Type[T], endpoint_base: str,
                              object_id: int, data: Dict[str, Any]) -> Optional[T]:
        """Perform a PATCH update sending only the fields to update."""
        cache = self._require_cache()
        payload = {k: v for k, v in data.items() if k not in ['id', 'created_at', 'updated_at']}

        flattened_payload = {}
        for key, value in payload.items():
            if isinstance(value, dict) and 'id' in value:
                flattened_payload[key] = value['id']
            else:
                flattened_payload[key] = value

        response_data = self._make_request(
            f"{endpoint_base}/{object_id}/", method="PATCH", data=flattened_payload
        )
        if response_data:
            obj = model_class(response_data, self)
            cache.set(model_class, obj.id, obj)
            return obj
        return None
