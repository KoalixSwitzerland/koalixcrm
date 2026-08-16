# -*- coding: utf-8 -*-
"""ADR-0009 / REQ-0018: `Location` n-level hierarchy helpers — cycle
detection for `clean()` and a single recursive-CTE breadcrumb query
(root -> node) for UC-0008/UC-0009 barcode resolution.

Justification: framework — raw WITH RECURSIVE SQL via django.db.connection; direct DB access is categorically forbidden to a microservice by ADR-0002 §1.3, so this cannot be reproduced outside Django; still needed with the microservice fleet deleted."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import connection
from django.utils.translation import gettext as _

if TYPE_CHECKING:
    from koalixcrm.stock.models.location import Location

_MAX_DEPTH_GUARD = 10_000

#: `Location.Meta.db_table`. SQL cannot bind a table name as a parameter, so
#: building the query below by interpolating `Model._meta.db_table` would mean
#: constructing SQL from a string — safe here, but indistinguishable to a
#: static analyser from the genuinely unsafe version, and a reviewer has to
#: re-derive the argument every time. Naming the table as a literal makes the
#: statement a constant with no construction at all; `test_location.py` asserts
#: it still matches `Meta.db_table`, so a rename fails a test rather than
#: producing a query against a table that no longer exists.
LOCATION_TABLE = "stock_location"

_ANCESTOR_PATH_SQL = """
    WITH RECURSIVE ancestors(id, parent_id, depth) AS (
        SELECT id, parent_id, 0 AS depth FROM stock_location WHERE id = %s
        UNION ALL
        SELECT l.id, l.parent_id, ancestors.depth + 1
        FROM stock_location l
        INNER JOIN ancestors ON l.id = ancestors.parent_id
    )
    SELECT id FROM ancestors ORDER BY depth DESC
"""


def assert_no_cycle(location: "Location") -> None:
    """Raise `ValidationError` if `location.parent` is `location` itself or
    if walking the `parent` chain from `location.parent` ever returns to
    `location` (direct or transitive self-ancestry)."""
    if location.parent_id is None:
        return
    if location.pk is not None and location.parent_id == location.pk:
        raise ValidationError(_("A Location cannot be its own parent."))
    ancestor = location.parent
    steps = 0
    while ancestor is not None:
        steps += 1
        if steps > _MAX_DEPTH_GUARD:
            raise ValidationError(_("Location parent chain exceeds the maximum supported depth."))
        if location.pk is not None and ancestor.pk == location.pk:
            raise ValidationError(_("Circular parent reference detected in the Location hierarchy."))
        ancestor = ancestor.parent


def get_ancestor_path(location: "Location") -> list["Location"]:
    """Return `[root, ..., location]` — the full path from the root node to
    `location` inclusive — using a single `WITH RECURSIVE` query for the id
    chain plus one hydration query, instead of one query per hierarchy
    level (REQ-0018 AC-2/Performance)."""
    from koalixcrm.stock.models.location import Location

    if location.pk is None:
        return [location]

    with connection.cursor() as cursor:
        cursor.execute(_ANCESTOR_PATH_SQL, [location.pk])
        ids_root_to_leaf = [row[0] for row in cursor.fetchall()]

    locations_by_id = {loc.pk: loc for loc in Location.objects.filter(pk__in=ids_root_to_leaf)}
    return [locations_by_id[i] for i in ids_root_to_leaf if i in locations_by_id]
