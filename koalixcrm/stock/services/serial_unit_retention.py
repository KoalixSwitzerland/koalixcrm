# -*- coding: utf-8 -*-
"""ADR-0012 Aufbewahrungsuntergrenze für `SerialUnit`: decommissioned rows
are retained forever by default; the workspace-configurable
`RetentionPolicy.serial_unit_retention_floor_days` is an additive
protection floor, not a deletion trigger. "Jede künftige
Lösch-Werkzeug-Implementierung MUSS das Löschen von `SerialUnit`-Zeilen
verweigern, deren `decommissioned_at` die konfigurierte Untergrenze noch
nicht unterschritten hat" (ADR-0012). `SerialUnit.delete()` calls
`assert_deletable()` so this refusal holds for every deletion path today,
not only a not-yet-built dedicated tool.

Justification: framework — deletion guard invoked from SerialUnit.delete() itself, same shape as movement_retention; still needed with the microservice fleet deleted."""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

if TYPE_CHECKING:
    from koalixcrm.core.models.workspace import Workspace
    from koalixcrm.stock.models.serial_unit import SerialUnit


def get_retention_floor_days(workspace: "Workspace") -> int | None:
    from koalixcrm.stock.models.retention_policy import RetentionPolicy

    policy = RetentionPolicy.objects.filter(workspace=workspace).first()
    return policy.serial_unit_retention_floor_days if policy else None


def assert_deletable(serial_unit: "SerialUnit") -> None:
    """Raise `ValidationError` unless `serial_unit` may be deleted: it must
    be decommissioned, and — if a retention floor is configured for its
    workspace — that floor must have elapsed since `decommissioned_at`."""
    if serial_unit.decommissioned_at is None:
        raise ValidationError(
            _("A SerialUnit must be decommissioned before it may be deleted.")
        )
    floor_days = get_retention_floor_days(serial_unit.workspace)
    if floor_days is not None:
        earliest = serial_unit.decommissioned_at + datetime.timedelta(days=floor_days)
        if timezone.now() < earliest:
            raise ValidationError(
                _("Retention floor has not yet elapsed for this SerialUnit; deletion is refused.")
            )
