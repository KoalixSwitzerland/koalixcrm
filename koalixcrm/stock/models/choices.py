# -*- coding: utf-8 -*-
"""Enum-style choice constants for the stock domain backbone.

Ratified by ADR-0009 (Lager-Domänen-Backbone, incl. Amendment 2026-05-04
`LAYER` and Amendment 2026-06-28 `ProductVariant` rekey) and ADR-0012
(Lebenszeit, Charge, Los und Seriennummernverfolgung, incl. Amendment
2026-07-04 `ProductVariant` rekey). `LocationType`-Enum-Werte are global,
platform-wide lookup values per the ADR-0009 Workspace-Scoping-Matrix — not
workspace-scoped rows.
"""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


class LocationType(models.TextChoices):
    """ADR-0009 + Amendment 2026-05-04: `LAYER` sits between `SHELF` and
    `BIN` to make the 4-level Regal->Fach->Ebene->Position hierarchy
    (UC-0008, UC-0009) machine-readable."""

    WAREHOUSE = "WAREHOUSE", _("Warehouse")
    ZONE = "ZONE", _("Zone")
    AISLE = "AISLE", _("Aisle")
    RACK = "RACK", _("Rack")
    SHELF = "SHELF", _("Shelf")
    LAYER = "LAYER", _("Layer")
    BIN = "BIN", _("Bin")
    VIRTUAL = "VIRTUAL", _("Virtual")
    CUSTOMER_SITE = "CUSTOMER_SITE", _("Customer Site")


class HandlingUnitType(models.TextChoices):
    """ADR-0009: `HandlingUnit.hu_type`."""

    PALLET = "PALLET", _("Pallet")
    CARTON = "CARTON", _("Carton")
    TRAY = "TRAY", _("Tray")
    CAGE = "CAGE", _("Cage")
    OTHER = "OTHER", _("Other")


class OwnerType(models.TextChoices):
    """ADR-0009: `OnHandRecord.owner_type`. `CUSTOMER_CONSIGNMENT`,
    `RENTAL` and `CUSTOMER_OWNED` require `owner_party` to be set (REQ-0019
    AC-1); `OWN` does not. `CUSTOMER_OWNED` is the ADR-0013 workshop/service
    case (customer owns, company holds with a return obligation) — the
    mirror image of `RENTAL` (company owns, customer holds)."""

    OWN = "OWN", _("Own")
    CUSTOMER_CONSIGNMENT = "CUSTOMER_CONSIGNMENT", _("Customer Consignment")
    RENTAL = "RENTAL", _("Rental")
    CUSTOMER_OWNED = "CUSTOMER_OWNED", _("Customer Owned")


class SerialConditionState(models.TextChoices):
    """ADR-0012: `SerialUnit.condition_state`; also the ADR-0013 rental
    fleet condition-tracking database basis."""

    NEW = "NEW", _("New")
    USED = "USED", _("Used")
    DAMAGED = "DAMAGED", _("Damaged")
    IN_REPAIR = "IN_REPAIR", _("In Repair")


class EventType(models.TextChoices):
    """ADR-0011: `StockMovement.event_type`, GS1 EPCIS 2.0 event types."""

    OBJECT_EVENT = "OBJECT_EVENT", _("Object Event")
    AGGREGATION_EVENT = "AGGREGATION_EVENT", _("Aggregation Event")
    TRANSACTION_EVENT = "TRANSACTION_EVENT", _("Transaction Event")
    TRANSFORMATION_EVENT = "TRANSFORMATION_EVENT", _("Transformation Event")
    ASSOCIATION_EVENT = "ASSOCIATION_EVENT", _("Association Event")


class BusinessStep(models.TextChoices):
    """ADR-0011: `StockMovement.business_step`, GS1 EPCIS CBV business-step
    codes plus the project-specific `inventorying` step (Amendment
    2026-05-04, OQ-0017; not a standard GS1 EPCIS 2.0 CBV code)."""

    SHIPPING = "shipping", _("Shipping")
    RECEIVING = "receiving", _("Receiving")
    PACKING = "packing", _("Packing")
    PICKING = "picking", _("Picking")
    ACCEPTING = "accepting", _("Accepting")
    INSPECTING = "inspecting", _("Inspecting")
    SCRAPPING = "scrapping", _("Scrapping")
    RETURNING = "returning", _("Returning")
    RENTAL_OUT = "rental_out", _("Rental Out")
    RENTAL_RETURN = "rental_return", _("Rental Return")
    ADJUSTMENT = "adjustment", _("Adjustment")
    COMMISSIONING = "commissioning", _("Commissioning")
    INSTALLING = "installing", _("Installing")
    REMOVING = "removing", _("Removing")
    REPAIRING = "repairing", _("Repairing")
    DECOMMISSIONING = "decommissioning", _("Decommissioning")
    INVENTORYING = "inventorying", _("Inventorying")


class Disposition(models.TextChoices):
    """ADR-0011 Amendment 2026-05-04 (OQ-0010): GS1 EPCIS CBV Disposition
    vocabulary; discriminates planned (`reserved`) vs. physical
    (`in_possession`) rental movements."""

    IN_PROGRESS = "in_progress", _("In Progress")
    RESERVED = "reserved", _("Reserved")
    IN_TRANSIT = "in_transit", _("In Transit")
    IN_POSSESSION = "in_possession", _("In Possession")
    RETURNED = "returned", _("Returned")
    DESTROYED = "destroyed", _("Destroyed")


class ReservationKind(models.TextChoices):
    """ADR-0010 Amendment 2026-05-04 (OQ-0013): `StockReservation.kind`."""

    SALE = "SALE", _("Sale")
    RENTAL = "RENTAL", _("Rental")
    PROJECT_HOLD = "PROJECT_HOLD", _("Project Hold")


class ReservationType(models.TextChoices):
    """ADR-0010: `StockReservation.reservation_type`."""

    BOOKED = "BOOKED", _("Booked")
    RESERVED_FOR_DOCUMENT = "RESERVED_FOR_DOCUMENT", _("Reserved For Document")


class ReservationConfirmationStatus(models.TextChoices):
    """ADR-0010 Amendment 2026-05-04 (OQ-0012):
    `StockReservation.reservation_status` — bindingness level, orthogonal
    to the `status` lifecycle field."""

    PROVISIONAL = "PROVISIONAL", _("Provisional")
    CONFIRMED = "CONFIRMED", _("Confirmed")


class ReservationLifecycleStatus(models.TextChoices):
    """ADR-0010: `StockReservation.status`."""

    ACTIVE = "ACTIVE", _("Active")
    FULFILLED = "FULFILLED", _("Fulfilled")
    CANCELLED = "CANCELLED", _("Cancelled")
    EXPIRED = "EXPIRED", _("Expired")


class RentalAssignmentStatus(models.TextChoices):
    """ADR-0013 Amendment 2026-05-04 (OQ-0013): `RentalAssignment.status`."""

    ACTIVE = "ACTIVE", _("Active")
    RETURNED = "RETURNED", _("Returned")
    OVERDUE = "OVERDUE", _("Overdue")
    WRITTEN_OFF = "WRITTEN_OFF", _("Written Off")


class GoodsReceiptStatus(models.TextChoices):
    """ADR-0017: `GoodsReceipt.status`."""

    DRAFT = "DRAFT", _("Draft")
    IN_PROGRESS = "IN_PROGRESS", _("In Progress")
    COMPLETED = "COMPLETED", _("Completed")
    CANCELLED = "CANCELLED", _("Cancelled")


class GoodsReceiptLineStatus(models.TextChoices):
    """ADR-0017: `GoodsReceiptLine.line_status`."""

    PENDING = "PENDING", _("Pending")
    CONFIRMED = "CONFIRMED", _("Confirmed")
    MISMATCHED = "MISMATCHED", _("Mismatched")


class ProductionOrderStatus(models.TextChoices):
    """ADR-0014: `ProductionOrder.status`."""

    DRAFT = "DRAFT", _("Draft")
    RELEASED = "RELEASED", _("Released")
    IN_PROGRESS = "IN_PROGRESS", _("In Progress")
    COMPLETED = "COMPLETED", _("Completed")
    CANCELLED = "CANCELLED", _("Cancelled")
