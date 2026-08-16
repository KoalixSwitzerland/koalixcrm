# -*- coding: utf-8 -*-
"""ADR-0012 / ADR-0021 application-layer invariant: `OnHandRecord` (and,
from Stage 5, `StockMovement`) rows must carry a `Batch`/`SerialUnit` FK
consistent with the referenced `ProductVariant.tracking_mode`:

- `tracking_mode = BATCH`  -> a `Batch` FK is required.
- `tracking_mode = SERIAL` -> a `SerialUnit` FK is required (and exactly
  one unit per record, `qty_on_hand = 1`).
- `tracking_mode = NONE`   -> neither FK may be set.

"The database schema alone offers no structural guarantee" (ADR-0012) —
this module is the enforcement point referenced by ADR-0012's Consequences
section and REQ-0022 AC-5.

Justification: framework — FK-consistency invariant enforced at Django model validation time (ADR-0012/ADR-0021), not expressible as a DB constraint; still needed with the microservice fleet deleted.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from koalixcrm.products.models.choices import TrackingMode

if TYPE_CHECKING:
    from koalixcrm.products.models.product_variant import ProductVariant
    from koalixcrm.stock.models.batch import Batch
    from koalixcrm.stock.models.serial_unit import SerialUnit


def enforce_tracking_mode_coupling(
    variant: "ProductVariant",
    batch: "Batch | None",
    serial_unit: "SerialUnit | None",
) -> None:
    mode = variant.tracking_mode
    if mode == TrackingMode.BATCH and batch is None:
        raise ValidationError(
            _("tracking_mode=BATCH requires a Batch reference.")
        )
    if mode == TrackingMode.SERIAL and serial_unit is None:
        raise ValidationError(
            _("tracking_mode=SERIAL requires a SerialUnit reference.")
        )
    if mode == TrackingMode.NONE and (batch is not None or serial_unit is not None):
        raise ValidationError(
            _("tracking_mode=NONE forbids Batch and SerialUnit references.")
        )
    if batch is not None and batch.variant_id != variant.id:
        raise ValidationError(
            _("Batch must belong to the same ProductVariant as the stock row.")
        )
    if serial_unit is not None and serial_unit.variant_id != variant.id:
        raise ValidationError(
            _("SerialUnit must belong to the same ProductVariant as the stock row.")
        )
