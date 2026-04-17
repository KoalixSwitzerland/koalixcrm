# -*- coding: utf-8 -*-
from koalixcrm.contacts.models.contact import *
from koalixcrm.contacts.models.customer_group import *
from koalixcrm.contacts.models.customer import *
from koalixcrm.contacts.models.postal_address import *
from koalixcrm.contacts.models.customer_billing_cycle import *
from koalixcrm.contacts.models.email_address import *
from koalixcrm.contacts.models.phone_address import *
from koalixcrm.contacts.models.supplier import *
from koalixcrm.contacts.models.person import *
from koalixcrm.contacts.models.call import *

# New Party-pattern models (issue #198 / PR #392). Coexist with the legacy
# models above until #395 drops them. Class names of the two models that
# collide with legacy (`Contact` → `PartyContact`, `EmailAddress` →
# `PartyEmail`) are transitional and get renamed in #395.
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
