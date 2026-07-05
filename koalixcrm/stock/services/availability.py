# -*- coding: utf-8 -*-
"""ADR-0010 Amendment 2026-05-04 (OQ-0011, rekeyed to `ProductVariant` by
Amendment 2026-07-04): time-window ATP for serial-tracked rental/
project-hold stock. `is_free()`/`free_windows()` are computed queries over
the canonical `StockReservation` table — no materialized
`UnitAvailabilityWindow` table.

Justification: framework — ORM-computed ATP query over StockReservation, exposed only as a synchronous GET read within the same Django app; still needed with the microservice fleet deleted since it serves an in-request availability check."""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from koalixcrm.stock.models.choices import ReservationKind, ReservationLifecycleStatus

if TYPE_CHECKING:
    from koalixcrm.products.models.product_variant import ProductVariant
    from koalixcrm.stock.models.serial_unit import SerialUnit


def _occupying_reservations_qs(serial_unit: "SerialUnit", start: datetime.datetime, end: datetime.datetime):
    from koalixcrm.stock.models.stock_reservation import StockReservation

    # Half-open interval intersection: [a, b) intersects [c, d) iff a < d and c < b.
    return StockReservation.objects.filter(
        workspace=serial_unit.workspace,
        serial_unit=serial_unit,
        status=ReservationLifecycleStatus.ACTIVE,
        kind__in=(ReservationKind.RENTAL, ReservationKind.PROJECT_HOLD),
        rental_start__lt=end,
        rental_end__gt=start,
    ).order_by("rental_start")


def is_free(serial_unit: "SerialUnit", start: datetime.datetime, end: datetime.datetime) -> bool:
    """True iff no active RENTAL/PROJECT_HOLD `StockReservation` intersects
    `[start, end)` for `serial_unit` (half-open interval, edge-touching
    windows do not intersect)."""
    return not _occupying_reservations_qs(serial_unit, start, end).exists()


def free_windows(
    variant: "ProductVariant", start: datetime.datetime, end: datetime.datetime
) -> list[tuple["SerialUnit", list[tuple[datetime.datetime, datetime.datetime]]]]:
    """For every `SerialUnit` of `variant`, return the free sub-windows
    inside `[start, end)`, carved out of the request window by every
    occupying reservation block of that unit."""
    from koalixcrm.stock.models.serial_unit import SerialUnit

    results: list[tuple[SerialUnit, list[tuple[datetime.datetime, datetime.datetime]]]] = []
    units = SerialUnit.objects.filter(workspace=variant.workspace, variant=variant).order_by("serial_number")
    for unit in units:
        blocks = list(_occupying_reservations_qs(unit, start, end))
        windows: list[tuple[datetime.datetime, datetime.datetime]] = []
        cursor = start
        for reservation in blocks:
            block_start = max(reservation.rental_start, start)
            block_end = min(reservation.rental_end, end)
            if block_start > cursor:
                windows.append((cursor, block_start))
            if block_end > cursor:
                cursor = block_end
        if cursor < end:
            windows.append((cursor, end))
        results.append((unit, windows))
    return results
