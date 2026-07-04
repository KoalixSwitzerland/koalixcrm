# -*- coding: utf-8 -*-
"""Enum-style choice constants for the product catalog backbone.

Ratified by ADR-0003 (Produkt-Katalog-Backbone). `kind` and
`lifecycle_status` values and lifecycle transitions are load-bearing for
downstream ADRs (ADR-0004..ADR-0008, ADR-0019); do not add or remove values
without an ADR amendment.
"""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductKind(models.TextChoices):
    """ADR-0003: classifies a `Product` for typed downstream branching
    (classification, pricing, BOM, service profile) without polymorphic
    model hierarchies or industry-specific subclasses."""

    SERVICE = "SERVICE", _("Service")
    TRADING_GOOD = "TRADING_GOOD", _("Trading Good")
    MANUFACTURED_GOOD = "MANUFACTURED_GOOD", _("Manufactured Good")
    KIT = "KIT", _("Kit")
    RAW_MATERIAL = "RAW_MATERIAL", _("Raw Material")


class ProductLifecycleStatus(models.TextChoices):
    """ADR-0003 §Lifecycle-Status-Werte.

    Allowed transitions (enforced in
    `koalixcrm.products.services.product_lifecycle`):
      DRAFT -> ACTIVE
      DRAFT -> EXTERNAL_ONLY
      ACTIVE -> DISCONTINUED
      DISCONTINUED -> ARCHIVED

    ARCHIVED -> ACTIVE, DISCONTINUED -> DRAFT, and EXTERNAL_ONLY -> anything
    else are explicitly disallowed.
    """

    DRAFT = "DRAFT", _("Draft")
    ACTIVE = "ACTIVE", _("Active")
    DISCONTINUED = "DISCONTINUED", _("Discontinued")
    ARCHIVED = "ARCHIVED", _("Archived")
    EXTERNAL_ONLY = "EXTERNAL_ONLY", _("External Only")


class ProductMediaType(models.TextChoices):
    """ADR-0003: `ProductMedia.media_type` knows exactly these three values;
    any other value is rejected by the system."""

    IMAGE = "image", _("Image")
    DATASHEET = "datasheet", _("Datasheet")
    CERTIFICATE = "certificate", _("Certificate")


class AttributeDataType(models.TextChoices):
    """ADR-0004: the eight data types an `AttributeDefinition` may declare.
    Each non-`json` type (other than `measure`, which is carried by the
    `decimal` value table + a `Unit` FK) has exactly one typed value table."""

    STRING = "string", _("String")
    INT = "int", _("Integer")
    DECIMAL = "decimal", _("Decimal")
    BOOL = "bool", _("Boolean")
    ENUM = "enum", _("Enum")
    MEASURE = "measure", _("Measure (decimal + unit)")
    REFERENCE = "reference", _("Reference")
    JSON = "json", _("JSON")


class ServiceBillingModel(models.TextChoices):
    """ADR-0007 / REQ-0016: `ServiceProfile.billing_model` knows exactly
    these four values."""

    FIXED = "fixed", _("Fixed")
    HOURLY = "hourly", _("Hourly")
    SUBSCRIPTION = "subscription", _("Subscription")
    TIERED = "tiered", _("Tiered")


class AttributeScope(models.TextChoices):
    """ADR-0004: governs whether an `AttributeDefinition` is global
    (platform-wide, fixture-shipped), workspace-defined (tenant admin), or
    inherited from a `ClassificationNode`."""

    GLOBAL = "GLOBAL", _("Global")
    WORKSPACE = "WORKSPACE", _("Workspace")
    INHERITED = "INHERITED", _("Inherited")


class TrackingMode(models.TextChoices):
    """ADR-0009 (introduced as `Product.tracking_mode`) / ADR-0009 Amendment
    2026-06-28 & ADR-0021 (rekeyed to `ProductVariant.tracking_mode`) /
    ADR-0012 (`Batch`/`SerialUnit` entities gated by this field).

    `NONE` — no batch or serial tracking. `BATCH` — `stock.Batch` FK required
    on tracked stock rows. `SERIAL` — `stock.SerialUnit` FK required. Default
    is `NONE`. ADR-0019: `kind = SERVICE` allows only `NONE`
    (`ProductKindPolicy.check_tracking_mode`)."""

    NONE = "NONE", _("None")
    BATCH = "BATCH", _("Batch")
    SERIAL = "SERIAL", _("Serial")


class KitMode(models.TextChoices):
    """ADR-0014: `Product.kit_mode`, evaluated by the application layer only
    for `kind = KIT`. `EXPLODE_ON_PICK` reads the `BillOfMaterialsExplosion`
    snapshot at pick time (no pre-staged stock); `PREASSEMBLE` requires a
    physical kit `OnHandRecord` created ahead of time."""

    EXPLODE_ON_PICK = "EXPLODE_ON_PICK", _("Explode On Pick")
    PREASSEMBLE = "PREASSEMBLE", _("Preassemble")
