# -*- coding: utf-8 -*-
"""ADR-0015: the five `SerialUnit` lifecycle query paths, all pure
projections over the immutable `StockMovement` log — no separate lifecycle
table. Every function is read-only and never writes.

1. `full_history`          — every StockMovement for the unit, ordered.
2. `as_built_bom`          — AGGREGATION_EVENT rows with this unit as parent.
3. `installed_components`  — AGGREGATION_EVENT graph traversal:
                             installing without a later removing.
4. `who_held_it_when`      — holder timeline from disposition/owner_party.
5. `where_was_it_when`     — location timeline from destination_location.

Justification: framework — read-only ORM projections over the StockMovement log, exposed only as synchronous GET actions within the same app; still needed with the microservice fleet deleted.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from koalixcrm.stock.models.choices import BusinessStep, Disposition, EventType

if TYPE_CHECKING:
    from koalixcrm.stock.models.serial_unit import SerialUnit


@dataclass(frozen=True)
class HolderWindow:
    holder_party_id: int
    holder_party: Any
    holder_from: Any
    holder_to: Any


@dataclass(frozen=True)
class LocationWindow:
    location_id: int | None
    location: Any
    location_from: Any
    location_to: Any


def full_history(serial_unit: "SerialUnit"):
    """ADR-0015 §Vollständige Einheitenhistorie: all StockMovement rows for
    this SerialUnit, ordered ascending by `occurred_at`."""
    from koalixcrm.stock.models.stock_movement import StockMovement

    return StockMovement.objects.filter(serial_unit=serial_unit).order_by("occurred_at", "id")


def as_built_bom(serial_unit: "SerialUnit"):
    """ADR-0015 §As-Built-BOM: AGGREGATION_EVENT rows with this SerialUnit
    as the parent (`parent_serial_unit`)."""
    from koalixcrm.stock.models.stock_movement import StockMovement

    return StockMovement.objects.filter(
        event_type=EventType.AGGREGATION_EVENT, parent_serial_unit=serial_unit,
    ).order_by("occurred_at", "id")


def installed_components(serial_unit: "SerialUnit"):
    """ADR-0015 §Aktuell installierte Komponenten: for every child
    SerialUnit aggregated to this parent via an `installing` event, keep it
    only if no later `removing` event exists for the same child."""
    from koalixcrm.stock.models.stock_movement import StockMovement

    installing = StockMovement.objects.filter(
        event_type=EventType.AGGREGATION_EVENT,
        parent_serial_unit=serial_unit,
        business_step=BusinessStep.INSTALLING,
    ).order_by("occurred_at", "id")

    result = []
    for movement in installing:
        child = movement.serial_unit
        if child is None:
            continue
        removed = StockMovement.objects.filter(
            event_type=EventType.AGGREGATION_EVENT,
            parent_serial_unit=serial_unit,
            serial_unit=child,
            business_step=BusinessStep.REMOVING,
            occurred_at__gt=movement.occurred_at,
        ).exists()
        if not removed:
            result.append(child)
    return result


def who_held_it_when(serial_unit: "SerialUnit") -> list[HolderWindow]:
    """ADR-0015 §Halter-Zeitleiste (Amendment OQ-0014): projection over
    `disposition ∈ {in_possession, returned}`, grouped into closed holder
    windows `(holder_party, from, to)`; `to = None` for the current
    holder."""
    from koalixcrm.stock.models.stock_movement import StockMovement

    movements = StockMovement.objects.filter(
        serial_unit=serial_unit,
        disposition__in=(Disposition.IN_POSSESSION, Disposition.RETURNED),
    ).order_by("occurred_at", "id")

    windows: list[HolderWindow] = []
    open_window: dict | None = None
    for movement in movements:
        if movement.disposition == Disposition.IN_POSSESSION:
            if open_window is not None:
                windows.append(HolderWindow(
                    holder_party_id=open_window["party"].pk if open_window["party"] else None,
                    holder_party=open_window["party"],
                    holder_from=open_window["from"],
                    holder_to=movement.occurred_at,
                ))
            open_window = {"party": movement.owner_party, "from": movement.occurred_at}
        elif movement.disposition == Disposition.RETURNED and open_window is not None:
            windows.append(HolderWindow(
                holder_party_id=open_window["party"].pk if open_window["party"] else None,
                holder_party=open_window["party"],
                holder_from=open_window["from"],
                holder_to=movement.occurred_at,
            ))
            open_window = None

    if open_window is not None:
        windows.append(HolderWindow(
            holder_party_id=open_window["party"].pk if open_window["party"] else None,
            holder_party=open_window["party"],
            holder_from=open_window["from"],
            holder_to=None,
        ))
    return windows


def where_was_it_when(serial_unit: "SerialUnit") -> list[LocationWindow]:
    """ADR-0015 §Standort-Zeitleiste: projection segmented on
    `destination_location` changes; rows with `destination_location = null`
    do not interrupt the running window. `to = None` for the current
    location."""
    from koalixcrm.stock.models.stock_movement import StockMovement

    movements = StockMovement.objects.filter(serial_unit=serial_unit).order_by("occurred_at", "id")

    windows: list[LocationWindow] = []
    current_location = None
    window_start = None
    for movement in movements:
        if movement.destination_location_id is None:
            continue
        if movement.destination_location_id != (current_location.pk if current_location else None):
            if current_location is not None:
                windows.append(LocationWindow(
                    location_id=current_location.pk,
                    location=current_location,
                    location_from=window_start,
                    location_to=movement.occurred_at,
                ))
            current_location = movement.destination_location
            window_start = movement.occurred_at

    if current_location is not None:
        windows.append(LocationWindow(
            location_id=current_location.pk,
            location=current_location,
            location_from=window_start,
            location_to=None,
        ))
    return windows
