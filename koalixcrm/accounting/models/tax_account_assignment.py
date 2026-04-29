# -*- coding: utf-8 -*-
"""Optional-peer linkage between `core.Tax` and `accounting.Account`.

Historically `core.Tax` carried two FKs (`account_activa`, `account_passiva`)
pointing at `accounting.Account`. That coupling broke the fork-isolation
invariant: WFS does not install `koalixcrm.accounting`, so `core.Tax` could
not migrate. CR-2c relocates the linkage here — one assignment row per Tax
stores the two accounts. When `accounting` is absent the row type does not
exist; `core.Tax` is then a pure tax-rate record.
"""

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.accounting.models.account import Account


class TaxAccountAssignment(models.Model):
    id = models.BigAutoField(primary_key=True)
    tax = models.OneToOneField(
        "core.Tax",
        on_delete=models.CASCADE,
        related_name="account_assignment",
        verbose_name=_("Tax"),
    )
    activa_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name=_("Activa Account"),
        related_name="tax_account_assignments_as_activa",
        null=True,
        blank=True,
    )
    passiva_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name=_("Passiva Account"),
        related_name="tax_account_assignments_as_passiva",
        null=True,
        blank=True,
    )

    class Meta:
        app_label = "accounting"
        verbose_name = _("Tax Account Assignment")
        verbose_name_plural = _("Tax Account Assignments")

    def __str__(self) -> str:
        return _("Accounting for tax: ") + str(self.tax)
