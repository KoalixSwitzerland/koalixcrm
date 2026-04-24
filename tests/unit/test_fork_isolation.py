# -*- coding: utf-8 -*-
"""CR-5: fork-isolation invariant.

The five apps copied into the WFS fork (``core``, ``contacts``,
``contracts``, ``djangoUserExtension``, ``products``) must not import
from ``reporting``, ``accounting``, or ``subscriptions`` — WFS does not
install those apps, and any accidental cross-import would break the
WFS build.

The test walks every ``*.py`` under those five app trees and asserts
the source text contains no forbidden ``koalixcrm.<forbidden_app>``
references, either in ``import``/``from ... import`` statements or in
``ForeignKey`` / model string references (e.g. ``'reporting.Project'``).
"""
from __future__ import annotations

import ast
import pathlib
import re

import pytest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
PUBLIC_APPS = ('core', 'contacts', 'contracts', 'djangoUserExtension', 'products')
FORBIDDEN_APPS = ('reporting', 'accounting', 'subscriptions')

# Matches 'reporting.Project', "accounting.Account", etc. inside string literals.
_STRING_MODEL_REF = re.compile(
    r"""['"](?:{})\.[A-Z]\w+['"]""".format('|'.join(FORBIDDEN_APPS))
)


def _iter_source_files(app_name: str):
    app_dir = REPO_ROOT / 'koalixcrm' / app_name
    for path in app_dir.rglob('*.py'):
        # Skip compiled cache and migrations (migrations may reference
        # historical app labels via swappable_dependency, which is benign).
        if '__pycache__' in path.parts:
            continue
        if 'migrations' in path.parts:
            continue
        yield path


def _forbidden_import_names(tree: ast.AST) -> list[str]:
    """Return forbidden import names found at MODULE level only.

    Lazy imports inside function bodies (the pattern prescribed by
    `docs/architecture/optional_apps.md` for optional-peer access) are
    intentionally not flagged — they never execute at module import time
    and only fire when the peer app is actually installed and the wrapping
    `apps.is_installed` branch admits them. A top-level import, by contrast,
    would fail at module load in a WFS deployment where the peer app is
    absent.
    """
    hits: list[str] = []
    for node in tree.body if isinstance(tree, ast.Module) else []:
        if isinstance(node, ast.Import):
            for alias in node.names:
                for forbidden in FORBIDDEN_APPS:
                    if alias.name == f'koalixcrm.{forbidden}' or alias.name.startswith(
                        f'koalixcrm.{forbidden}.'
                    ):
                        hits.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for forbidden in FORBIDDEN_APPS:
                if module == f'koalixcrm.{forbidden}' or module.startswith(
                    f'koalixcrm.{forbidden}.'
                ):
                    hits.append(module)
    return hits


@pytest.mark.parametrize('app_name', PUBLIC_APPS)
def test_public_app_has_no_forbidden_imports(app_name: str):
    offenders: list[tuple[pathlib.Path, list[str]]] = []
    for path in _iter_source_files(app_name):
        source = path.read_text(encoding='utf-8')
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError:
            continue
        hits = _forbidden_import_names(tree)
        if hits:
            offenders.append((path, sorted(set(hits))))

    assert not offenders, (
        f"{app_name} imports from forbidden apps {FORBIDDEN_APPS}:\n"
        + '\n'.join(f"  {p.relative_to(REPO_ROOT)}: {hits}" for p, hits in offenders)
    )


@pytest.mark.parametrize('app_name', PUBLIC_APPS)
def test_public_app_has_no_forbidden_string_model_refs(app_name: str):
    """Catch ForeignKey('reporting.Project', …) and similar string refs."""
    offenders: list[tuple[pathlib.Path, list[str]]] = []
    for path in _iter_source_files(app_name):
        source = path.read_text(encoding='utf-8')
        hits = _STRING_MODEL_REF.findall(source)
        if hits:
            offenders.append((path, sorted(set(hits))))

    assert not offenders, (
        f"{app_name} references forbidden app models via string FK targets:\n"
        + '\n'.join(f"  {p.relative_to(REPO_ROOT)}: {hits}" for p, hits in offenders)
    )
