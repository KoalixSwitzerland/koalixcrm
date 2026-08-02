"""
Pagination classes for the koalixcrm REST API.

See ADR-0023 (Pagination Requires a Total Ordering) in the koalixcrm-system
documentation repository for the reasoning behind the enforcement point.
"""
from __future__ import annotations

from django.db.models import QuerySet
from rest_framework.pagination import PageNumberPagination


def _ordering_already_has_pk(order_by, pk_name):
    """True if `order_by` already references the model's primary key, in
    either sort direction, at any position.

    Entries are usually plain field-name strings ('-created_at',
    'party__name'), but Django also permits expression objects
    (``F('x').desc()``, ``Coalesce(...)``). Those are not field names and must
    neither be mistaken for the primary key nor raise.
    """
    for entry in order_by:
        if not isinstance(entry, str):
            continue
        if entry.removeprefix('-') in ('pk', pk_name):
            return True
    return False


class TotalOrderingPageNumberPagination(PageNumberPagination):
    """Page-number pagination that guarantees a total ordering.

    ``LIMIT``/``OFFSET`` paging over an ordering clause that lets two distinct
    rows compare equal is unsafe: the database may place tied rows differently
    from one page query to the next, so a row can be served on two pages while
    another is served on none. A client walking every page then double-counts
    one row and never sees the other — silently, and with plausible-looking
    totals.

    ``paginate_queryset()`` therefore appends the primary key as the final
    tiebreaker to the effective ordering, unless it is already part of it. The
    effective ordering is ``queryset.query.order_by``, falling back to
    ``model._meta.ordering``. Existing sort keys keep their position and
    direction; only tie-breaking changes.

    Custom pagination classes in this codebase inherit from this class rather
    than from ``PageNumberPagination`` directly, so a class written for an
    unrelated reason cannot silently drop the guarantee.
    """

    def paginate_queryset(self, queryset, request, view=None):
        queryset = self._ensure_total_ordering(queryset)
        return super().paginate_queryset(queryset, request, view=view)

    @staticmethod
    def _ensure_total_ordering(queryset):
        # DRF also paginates plain lists; only QuerySets carry .query/.model.
        if not isinstance(queryset, QuerySet):
            return queryset

        model = queryset.model
        pk_name = model._meta.pk.name
        effective_order_by = queryset.query.order_by or model._meta.ordering or ()

        if _ordering_already_has_pk(effective_order_by, pk_name):
            return queryset

        # query.order_by can be empty while Meta.ordering is set (Django
        # applies it lazily), so pass the effective clause explicitly to keep
        # the fallback verbatim and append nothing but the primary key.
        return queryset.order_by(*effective_order_by, 'pk')
