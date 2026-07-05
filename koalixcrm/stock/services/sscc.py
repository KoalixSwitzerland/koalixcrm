# -*- coding: utf-8 -*-
"""ADR-0009 Standards-Verankerung: `HandlingUnit.sscc` is a GS1 SSCC-18 —
an 18-digit numeric string (extension digit + GS1 company prefix + serial
reference + check digit).

Justification: framework — pure regex validator wired as a Django field/model validator inside full_clean(); still needed with the microservice fleet deleted."""
from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

_SSCC_RE = re.compile(r"^\d{18}$")


def validate_sscc(value: str) -> None:
    if not _SSCC_RE.match(value or ""):
        raise ValidationError(
            _("%(value)s is not a valid GS1 SSCC-18 (must be exactly 18 digits).")
            % {"value": value}
        )
