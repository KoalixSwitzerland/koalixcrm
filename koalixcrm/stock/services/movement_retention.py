# -*- coding: utf-8 -*-
"""ADR-0011 Aufbewahrungsuntergrenze für `StockMovement`: the event log is
retained forever by default; the workspace-configurable
`RetentionPolicy.stock_movement_retention_floor_days` is an additive
protection floor, not a deletion trigger. "Jede künftige
Lösch-Werkzeug-Implementierung MUSS das Löschen von `StockMovement`-Zeilen
verweigern, deren `occurred_at` die konfigurierte Untergrenze noch nicht
unterschritten hat" (ADR-0011). `StockMovement.delete()` calls
`assert_deletable()` so this refusal holds for every deletion path."""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

if TYPE_CHECKING:
    from koalixcrm.core.models.workspace import Workspace
    from koalixcrm.stock.models.stock_movement import StockMovement


def get_retention_floor_days(workspace: "Workspace") -> int | None:
    from koalixcrm.stock.models.retention_policy import RetentionPolicy

    policy = RetentionPolicy.objects.filter(workspace=workspace).first()
    return policy.stock_movement_retention_floor_days if policy else None


def assert_deletable(movement: "StockMovement") -> None:
    """Raise `ValidationError` unless `movement` may be deleted: the
    default is refusal (movements are immutable/append-only); if a
    retention floor is configured, deletion is refused unless the floor has
    elapsed since `occurred_at`. In practice this means: with the default
    (no floor configured) deletion is still always refused, because
    `StockMovement` rows are immutable by design (ADR-0011) — this
    function exists so a future, explicitly-authorized deletion tool has a
    single place to consult, mirroring `serial_unit_retention`."""
    floor_days = get_retention_floor_days(movement.workspace)
    if floor_days is None:
        raise ValidationError(
            _("StockMovement rows are immutable and append-only; deletion is refused.")
        )
    earliest = movement.occurred_at + datetime.timedelta(days=floor_days)
    if timezone.now() < earliest:
        raise ValidationError(
            _("Retention floor has not yet elapsed for this StockMovement; deletion is refused.")
        )
