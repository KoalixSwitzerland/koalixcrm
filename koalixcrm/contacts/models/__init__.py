# -*- coding: utf-8 -*-
"""koalixcrm.contacts models (post-v2.0.0 / issue #395 G3).

Legacy Contact/Customer/Supplier/Person/CustomerGroup/Call models are
gone. `PostalAddress`/`PhoneAddress`/`EmailAddress` are retained as
MTI base classes for non-legacy satellite tables in `contracts` and
`djangoUserExtension` — those inherit field layout, not Party-domain
semantics.

Transitional class names `PartyContact` and `PartyEmail` are to be
renamed to `Contact` and `EmailAddress` in a follow-up step of G3
(G4: rename pass).
"""
from koalixcrm.contacts.models.customer_billing_cycle import *  # noqa: F401, F403

# Shared MTI base classes retained for contracts / djangoUserExtension
# satellite tables (not "legacy" — reusable field layouts).
from koalixcrm.contacts.models.postal_address import *  # noqa: F401, F403
from koalixcrm.contacts.models.email_address import *  # noqa: F401, F403
from koalixcrm.contacts.models.phone_address import *  # noqa: F401, F403

# Party data model (issue #198).
from koalixcrm.contacts.models.party import *  # noqa: F401, F403
from koalixcrm.contacts.models.organization import *  # noqa: F401, F403
from koalixcrm.contacts.models.natural_person import *  # noqa: F401, F403
from koalixcrm.contacts.models.party_identification import *  # noqa: F401, F403
from koalixcrm.contacts.models.party_role import *  # noqa: F401, F403
from koalixcrm.contacts.models.organization_membership import *  # noqa: F401, F403
from koalixcrm.contacts.models.organization_relationship import *  # noqa: F401, F403
from koalixcrm.contacts.models.address import *  # noqa: F401, F403
from koalixcrm.contacts.models.address_assignment import *  # noqa: F401, F403
from koalixcrm.contacts.models.phone_number import *  # noqa: F401, F403
from koalixcrm.contacts.models.phone_assignment import *  # noqa: F401, F403
from koalixcrm.contacts.models.party_email import *  # noqa: F401, F403
from koalixcrm.contacts.models.email_assignment import *  # noqa: F401, F403
from koalixcrm.contacts.models.party_group import *  # noqa: F401, F403
from koalixcrm.contacts.models.party_group_membership import *  # noqa: F401, F403
