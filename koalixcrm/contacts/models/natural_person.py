# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.contacts.models.party import Party
from koalixcrm.core.const.postaladdressprefix import POSTALADDRESSPREFIX
from koalixcrm.core.const.party import LANGUAGE_CHOICES


# Class is named `PartyContact` (not `Contact`) to avoid colliding with the
# legacy `koalixcrm.contacts.models.contact.Contact` during the #392..#394
# coexistence phase. Both class and file are renamed to `Contact` / `contact.py`
# in #395 after the legacy model is dropped.
class PartyContact(Party):
    prefix = models.CharField(
        max_length=1, choices=POSTALADDRESSPREFIX,
        blank=True, null=True,
        verbose_name=_("Prefix"),
    )
    given_name = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_("Given name"),
    )
    family_name = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_("Family name"),
    )
    date_of_birth = models.DateField(
        blank=True, null=True,
        verbose_name=_("Date of birth"),
    )
    gdpr_consent_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("GDPR consent date"),
    )
    preferred_language = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES,
        blank=True, null=True,
        verbose_name=_("Preferred language"),
    )

    class Meta:
        app_label = "contacts"
        db_table = "crm_partycontact"
        verbose_name = _("Contact (Person)")
        verbose_name_plural = _("Contacts (People)")
