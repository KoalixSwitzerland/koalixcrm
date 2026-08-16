# -*- coding: utf-8 -*-
"""Lifecycle transition rules for `products.Product`.

ADR-0003 §Lifecycle-Status-Werte. Business logic lives here (not in the
view/serializer) so it can be invoked identically from `Product.clean()`,
the admin, and DRF serializers.

Justification: framework — shared validation source invoked identically from Product.clean(), the admin and DRF serializers; still needed with the microservice fleet deleted.
"""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from koalixcrm.products.models.choices import ProductLifecycleStatus

# Allowed forward transitions. Any (old, new) pair not listed here — other
# than a no-op (old == new) — is rejected.
ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    ProductLifecycleStatus.DRAFT: frozenset({
        ProductLifecycleStatus.ACTIVE,
        ProductLifecycleStatus.EXTERNAL_ONLY,
    }),
    ProductLifecycleStatus.ACTIVE: frozenset({
        ProductLifecycleStatus.DISCONTINUED,
    }),
    ProductLifecycleStatus.DISCONTINUED: frozenset({
        ProductLifecycleStatus.ARCHIVED,
    }),
    ProductLifecycleStatus.ARCHIVED: frozenset(),
    ProductLifecycleStatus.EXTERNAL_ONLY: frozenset(),
}


def validate_lifecycle_transition(old_status: str | None, new_status: str) -> None:
    """Raise `ValidationError` if `old_status` -> `new_status` is not an
    ADR-0003-allowed transition.

    `old_status is None` means the object is being created for the first
    time; any valid enum value is accepted as an initial status.
    """
    if old_status is None or old_status == new_status:
        return
    allowed = ALLOWED_TRANSITIONS.get(old_status, frozenset())
    if new_status not in allowed:
        raise ValidationError(
            {
                "lifecycle_status": _(
                    "Illegal lifecycle transition from %(old)s to %(new)s."
                ) % {"old": old_status, "new": new_status}
            }
        )
