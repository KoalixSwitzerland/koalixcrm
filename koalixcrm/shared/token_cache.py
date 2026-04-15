# -*- coding: utf-8 -*-
"""
Singleton token cache for M2M authentication tokens.
Ported from qq_workflow_support_webapp_backend.

Simplified version without SSM Parameter Store dependency.
Uses local file persistence only.
"""
import os
import time
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class TokenCache:
    """
    Singleton cache for M2M authentication tokens.

    Persistence: local file (m2m_token.env).
    """
    _instance = None
    _token_type = "Bearer"
    _access_token = None
    _identity_token = None
    _expires_at = 0  # Unix timestamp

    ENV_VAR_ACCESS_TOK = "M2M_CACHED_ACCESS_TOKEN"
    ENV_VAR_IDENTITY_TOK = "M2M_CACHED_IDENTITY_TOKEN"
    ENV_VAR_TOK_EXP = "M2M_CACHED_TOKEN_EXPIRES"
    ENV_VAR_TOK_TYPE = "M2M_CACHED_TOKEN_TYPE"

    ENV_TOKEN_FILE = "m2m_token.env"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_from_file()
        return cls._instance

    def _load_from_file(self) -> bool:
        if not os.path.exists(self.ENV_TOKEN_FILE):
            return False
        try:
            with open(self.ENV_TOKEN_FILE, 'r') as f:
                env_data = {}
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        env_data[key] = value

            access_token = env_data.get(self.ENV_VAR_ACCESS_TOK)
            expires_at_str = env_data.get(self.ENV_VAR_TOK_EXP)

            if access_token and expires_at_str:
                self._access_token = access_token
                self._identity_token = env_data.get(self.ENV_VAR_IDENTITY_TOK)
                self._expires_at = int(expires_at_str)
                self._token_type = env_data.get(self.ENV_VAR_TOK_TYPE, "Bearer")
                logger.info("Loaded token from %s", self.ENV_TOKEN_FILE)
                return True
        except Exception as e:
            logger.error("Error loading token from %s: %s", self.ENV_TOKEN_FILE, e)
        return False

    def save_to_file(self):
        if not self._access_token or not self._expires_at:
            return False
        try:
            os.makedirs(
                os.path.dirname(os.path.abspath(self.ENV_TOKEN_FILE)),
                exist_ok=True,
            )
            with open(self.ENV_TOKEN_FILE, 'w') as f:
                f.write(f"{self.ENV_VAR_ACCESS_TOK}={self._access_token}\n")
                f.write(f"{self.ENV_VAR_TOK_TYPE}={self._token_type}\n")
                f.write(f"{self.ENV_VAR_TOK_EXP}={self._expires_at}\n")
                if self._identity_token:
                    f.write(f"{self.ENV_VAR_IDENTITY_TOK}={self._identity_token}\n")
            logger.info("Saved token to %s", self.ENV_TOKEN_FILE)
            return True
        except Exception as e:
            logger.error("Error saving token to %s: %s", self.ENV_TOKEN_FILE, e)
            return False

    def get_token(self) -> Optional[Tuple[str, str]]:
        """Return (access_token, token_type) if valid, else None."""
        if self._access_token and time.time() < self._expires_at:
            return self._access_token, self._token_type
        return None

    def set_token(
        self,
        access_token: str,
        token_type: str,
        identity_token: Optional[str] = None,
        save_to_env: bool = False,
    ):
        """Cache a token and optionally persist to file."""
        self._access_token = access_token
        self._identity_token = identity_token
        self._token_type = token_type

        try:
            import jwt
            payload = jwt.decode(
                access_token, algorithms=["RS256"],
                options={"verify_signature": False},
            )
            self._expires_at = payload.get('exp', int(time.time()) + 3600)
        except Exception as e:
            logger.warning("Error parsing token expiration: %s", e)
            self._expires_at = int(time.time()) + 3600

        if save_to_env:
            self.save_to_file()

    def store_token(self, access_token: str, token_type: str, expires_in: int):
        """Store a token with an explicit expires_in (seconds)."""
        self._access_token = access_token
        self._token_type = token_type
        self._expires_at = int(time.time()) + expires_in - 60
        self.save_to_file()

    def clear(self):
        """Clear cached token from memory and local file."""
        self._access_token = None
        self._identity_token = None
        self._token_type = None
        self._expires_at = 0

        if os.path.exists(self.ENV_TOKEN_FILE):
            try:
                os.remove(self.ENV_TOKEN_FILE)
            except (OSError, PermissionError):
                pass
