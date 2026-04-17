# -*- coding: utf-8 -*-
"""Choice constants for the Party data model (issue #198, PR #392).

Kept in `core.const` so choices are shared between models, admin, serializers,
and future UBL export without circular imports.
"""
from django.utils.translation import gettext_lazy as _

PARTY_ROLE_CUSTOMER = 'customer'
PARTY_ROLE_SUPPLIER = 'supplier'
PARTY_ROLE_LEAD = 'lead'
PARTY_ROLE_PROSPECT = 'prospect'
PARTY_ROLE_EMPLOYEE = 'employee'
PARTY_ROLE_PARTNER = 'partner'
PARTY_ROLE_BANK = 'bank'
PARTY_ROLE_AUTHORITY = 'authority'

PARTY_ROLE_CHOICES = (
    (PARTY_ROLE_CUSTOMER, _('Customer')),
    (PARTY_ROLE_SUPPLIER, _('Supplier')),
    (PARTY_ROLE_LEAD, _('Lead')),
    (PARTY_ROLE_PROSPECT, _('Prospect')),
    (PARTY_ROLE_EMPLOYEE, _('Employee')),
    (PARTY_ROLE_PARTNER, _('Partner')),
    (PARTY_ROLE_BANK, _('Bank')),
    (PARTY_ROLE_AUTHORITY, _('Authority')),
)

IDENTIFICATION_SCHEME_CHOICES = (
    ('internal', _('Internal ID')),
    ('vat', _('VAT')),
    ('uid', _('Swiss UID')),
    ('gln', _('GLN')),
    ('duns', _('DUNS')),
    ('lei', _('LEI')),
    ('iban', _('IBAN')),
)

ORG_RELATIONSHIP_CHOICES = (
    ('parent_of', _('Parent of')),
    ('subsidiary_of', _('Subsidiary of')),
    ('partner_of', _('Partner of')),
    ('franchise_of', _('Franchise of')),
)

ASSIGNMENT_PURPOSE_CHOICES = (
    ('primary', _('Primary')),
    ('billing', _('Billing')),
    ('shipping', _('Shipping')),
    ('legal', _('Legal / registered seat')),
    ('visit', _('Visiting')),
    ('other', _('Other')),
)

LEGAL_FORM_CHOICES = (
    ('ag', _('AG')),
    ('gmbh', _('GmbH')),
    ('verein', _('Verein')),
    ('stiftung', _('Stiftung')),
    ('einzelfirma', _('Einzelfirma')),
    ('holding', _('Holding')),
    ('kg', _('KG')),
    ('ag_co_kg', _('AG & Co. KG')),
    ('public', _('Public body')),
    ('other', _('Other')),
)

LANGUAGE_CHOICES = (
    ('de', _('German')),
    ('fr', _('French')),
    ('it', _('Italian')),
    ('en', _('English')),
)
