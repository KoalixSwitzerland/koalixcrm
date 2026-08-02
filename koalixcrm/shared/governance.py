# -*- coding: utf-8 -*-
"""Master-data governance registry (ADR-0024 §2).

Splits the products/stock domain into two classes with very different blast
radii:

* **schema models** define the vocabulary — what a product *is*. A mistake
  here is structural: it affects every product bound to the affected set,
  compounds silently, and is only repairable by migrating live tenant data.
* **instance models** carry the data itself. A mistake here is local, cheap
  and self-correcting.

Write access to the first class is granted separately from, and far more
sparingly than, the second. Many people create products; very few define
what a product is.

**Why Django model permissions rather than the `Role` enum.**
`core.access.permissions_for_role()` and `effective_roles()` look like the
natural home for this, but neither is consumed by anything outside its own
tests — the enum is currently decorative. Real enforcement runs through
`ModelPermissionsWithListView` (DRF's `DjangoModelPermissions`) against
Django's per-model permissions, in both the admin and the API. Expressing
the split there means it is enforced the day it lands rather than the day
someone wires the roles up.
"""
from __future__ import annotations

from django.apps import apps

#: Models that define vocabulary rather than carry data (ADR-0024 §2).
#: `(app_label, model_name)`, lower-cased to match Django's own conventions.
SCHEMA_MODELS: frozenset[tuple[str, str]] = frozenset({
    ('products', 'attributedefinition'),
    ('products', 'attributegroup'),
    ('products', 'attributeset'),
    ('products', 'attributesetgroup'),
    ('products', 'attributesetdefault'),
    ('products', 'attributevalidationrule'),
    ('products', 'classification'),
    ('products', 'classificationnode'),
    ('products', 'productattributemapping'),
})

#: Domains the schema/instance split is defined over. Models outside these
#: apps are out of scope and are neither schema nor instance here.
GOVERNED_APP_LABELS: frozenset[str] = frozenset({'products', 'stock'})

#: Django group holding write access to the vocabulary.
SCHEMA_AUTHOR_GROUP = 'catalog-schema-authors'

#: Django group holding write access to catalogue and stock data, and
#: read-only access to the vocabulary that shapes it.
DATA_EDITOR_GROUP = 'catalog-data-editors'

_WRITE_PERMISSIONS = ('add', 'change', 'delete')
_READ_PERMISSION = 'view'


def is_schema_model(model) -> bool:
    """True when `model` defines vocabulary rather than carrying data."""
    meta = model._meta
    return (meta.app_label, meta.model_name) in SCHEMA_MODELS


def governed_models() -> list:
    """Every concrete model in the governed apps, schema and instance alike."""
    return [
        model
        for app_label in sorted(GOVERNED_APP_LABELS)
        for model in apps.get_app_config(app_label).get_models()
    ]


def schema_models() -> list:
    return [model for model in governed_models() if is_schema_model(model)]


def instance_models() -> list:
    return [model for model in governed_models() if not is_schema_model(model)]


def unknown_schema_entries() -> set[tuple[str, str]]:
    """Entries in `SCHEMA_MODELS` that match no installed model.

    A rename that leaves a stale entry behind would silently drop that model
    back into the permissive class, so this is asserted rather than assumed.
    """
    installed = {(m._meta.app_label, m._meta.model_name) for m in governed_models()}
    return set(SCHEMA_MODELS) - installed
