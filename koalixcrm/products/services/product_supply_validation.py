# -*- coding: utf-8 -*-
"""ADR-0006 / REQ-0014 AC-2: `ProductSupply.supplier` must carry an active
`PartyRole` with `role_type = 'supplier'`. Enforced in the application layer
(serializer/service), not as a database constraint, per REQ-0014 AC-2.

Justification: framework — ORM PartyRole existence check enforced inline at write time in the serializer/service layer per REQ-0014 AC-2; still needed with the microservice fleet deleted."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from koalixcrm.core.const.party import PARTY_ROLE_SUPPLIER

if TYPE_CHECKING:
    from koalixcrm.contacts.models.party import Party


def validate_supplier_role(party: "Party") -> None:
    """Raise `ValidationError` if `party` has no active `supplier` role."""
    if not party.roles.filter(role_type=PARTY_ROLE_SUPPLIER).exists():
        raise ValidationError(
            _("%(party)s does not carry an active supplier PartyRole.") % {"party": party}
        )
