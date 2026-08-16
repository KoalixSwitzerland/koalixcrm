# -*- coding: utf-8 -*-
"""Structural field filtering for the koalixcrm REST API.

`AutoFilterBackend` derives a FilterSet from the model when a ViewSet does
not declare one, so that a resource is filterable by default rather than
because its author remembered to say so. This follows the enforcement
reasoning of ADR-0023: a rule that only holds when every author applies it
by hand erodes, and it erodes silently — an unfiltered list endpoint does
not raise, it returns the whole table and lets the caller believe it asked
a narrower question.

Exposed automatically, all with equality-style lookups only:

- foreign keys (`?product=5`) — the parent/child navigation that replaces
  nested routes,
- fields carrying `choices` (`?kind=SERVICE`) — bounded, low-cardinality,
- `CharField` and its subclasses (`?sku=…`, `?language_code=de`,
  `?gtin=…`) — the identifier columns that scan, catalogue and lookup
  flows are keyed on,
- booleans (`?is_active=true`),
- dates and datetimes with range lookups (`?valid_from__lte=…`),
- the primary key, for batch reads (`?id__in=1,2,3`).

`TextField` is the one field type left out: it holds prose (descriptions,
notes), where an exact match is not a question anyone asks.

Note what is *not* the reason for that exclusion. An `exact` match on an
unindexed column costs a sequential scan — but so does the unfiltered list
of the same table, which this API already serves, so filtering never makes
a request more expensive than the one it replaces. The cost argument
applies to substring lookups (`icontains`, `startswith`), which is why none
are generated here. Substring search belongs to `SearchFilter` with an
explicit `search_fields`, a per-resource decision about which columns are
worth an index.

A ViewSet that sets `filterset_fields` or `filterset_class` keeps full
control; this backend then defers to it unchanged.
"""
from __future__ import annotations

from django.db import models
from django_filters import rest_framework as django_filters

#: `workspace` is already applied by `WorkspaceScopedViewSetMixin.get_queryset`
#: and is implied by the URL prefix, so exposing it as a query parameter would
#: add a filter that can only ever narrow an already-narrowed queryset.
EXCLUDED_FIELD_NAMES = frozenset({'workspace'})

_RELATION_LOOKUPS = ['exact', 'in']
_CHOICE_LOOKUPS = ['exact', 'in']
_TEXT_LOOKUPS = ['exact', 'in']
_BOOLEAN_LOOKUPS = ['exact']
_TEMPORAL_LOOKUPS = ['exact', 'gte', 'lte']
_PK_LOOKUPS = ['exact', 'in']


def auto_filter_fields(model: type[models.Model]) -> dict[str, list[str]]:
    """Return the `filterset_fields` mapping derived from `model`.

    Concrete local fields only — reverse relations and many-to-many are left
    out, because filtering a list by a reverse relation produces duplicate
    rows unless the queryset is also distinct-ed, and that is a per-endpoint
    decision rather than a safe default.
    """
    fields: dict[str, list[str]] = {}

    for field in model._meta.get_fields():
        if not getattr(field, 'concrete', False):
            continue
        if field.name in EXCLUDED_FIELD_NAMES:
            continue

        if field.primary_key:
            fields[field.name] = list(_PK_LOOKUPS)
        elif field.is_relation and (field.many_to_one or field.one_to_one):
            fields[field.name] = list(_RELATION_LOOKUPS)
        elif getattr(field, 'choices', None):
            fields[field.name] = list(_CHOICE_LOOKUPS)
        elif isinstance(field, models.BooleanField):
            fields[field.name] = list(_BOOLEAN_LOOKUPS)
        elif isinstance(field, models.TextField):
            # `TextField` is a sibling of `CharField`, not a subclass, so it
            # would fall through anyway. Rejecting it by name states the
            # intent: prose is excluded on purpose, not by accident of the
            # type hierarchy.
            continue
        elif isinstance(field, models.CharField):
            # Covers the CharField subclasses too (EmailField, SlugField,
            # URLField), which are identifiers by nature.
            fields[field.name] = list(_TEXT_LOOKUPS)
        elif isinstance(field, models.DateField):
            # DateTimeField subclasses DateField, so this covers both.
            fields[field.name] = list(_TEMPORAL_LOOKUPS)

    return fields


class AutoFilterBackend(django_filters.DjangoFilterBackend):
    """`DjangoFilterBackend` with a model-derived default FilterSet.

    `get_filterset_class` is the override point rather than
    `filter_queryset`, because drf-spectacular's filter extension calls the
    same method to document the query parameters. Deriving the FilterSet
    here therefore keeps the published schema and the runtime behaviour from
    drifting apart — the parameters the API accepts are exactly the ones it
    advertises.

    **The derived class is deliberately not cached.** django-filter turns a
    foreign key into a `ModelChoiceFilter` whose choices come from the
    related model's `_default_manager`, and on `WorkspaceScopedModel` that
    manager is `WorkspaceAwareManager` — it reads the active workspace from
    a ContextVar and filters at the moment the queryset is built. Building
    the class per request means that read happens inside the request, with
    the workspace `WorkspaceContextMiddleware` activated. Memoising the
    class on the model would freeze one tenant's choice list into every
    later request for every other tenant, which fails as a wrongly rejected
    filter value at best and a cross-workspace disclosure at worst. The
    rebuild is a metaclass pass over one model's fields; that is the price
    of the guarantee, and it is the right trade.
    """

    def get_filterset_class(self, view, queryset=None):
        declares_own = (
            getattr(view, 'filterset_class', None) is not None
            or getattr(view, 'filterset_fields', None) is not None
        )
        if declares_own or queryset is None:
            return super().get_filterset_class(view, queryset)

        fields = auto_filter_fields(queryset.model)
        if not fields:
            return None

        meta = type('Meta', (), {'model': queryset.model, 'fields': fields})
        return type(
            f'{queryset.model.__name__}AutoFilterSet',
            (django_filters.FilterSet,),
            {'Meta': meta},
        )
