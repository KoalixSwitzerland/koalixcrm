# -*- coding: utf-8 -*-
"""Shared helpers for per-app peer-dependency declarations.

Each koalixcrm AppConfig declares `required_peers` (startup failure if any are
missing from INSTALLED_APPS) and optionally `optional_peers` (informational).
The `register_peer_check` helper attaches a Django system check that enforces
the `required_peers` list, so missing hard dependencies surface at startup
rather than first-request time.

See `docs/architecture/optional_apps.md` for the full pattern.
"""
from __future__ import annotations

from django.apps import AppConfig, apps
from django.core.checks import Error, register


def register_peer_check(app_config: AppConfig) -> None:
    required = tuple(getattr(app_config, 'required_peers', ()) or ())
    if not required:
        return

    @register()
    def _check_required_peers(app_configs, **kwargs):
        errors = []
        for peer in required:
            if not apps.is_installed(peer):
                errors.append(Error(
                    f"'{app_config.name}' requires '{peer}' in INSTALLED_APPS.",
                    hint=(
                        f"Add '{peer}' to INSTALLED_APPS, or remove "
                        f"'{app_config.name}' from INSTALLED_APPS."
                    ),
                    id=f'{app_config.label}.E001',
                ))
        return errors
