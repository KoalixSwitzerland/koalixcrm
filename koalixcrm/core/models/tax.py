# -*- coding: utf-8 -*-

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _


class Tax(models.Model):
    """Tax rate record. Historically carried FKs to `accounting.Account`;
    those linkages have been relocated to `accounting.TaxAccountAssignment`
    (CR-2c) so the model is usable in deployments that do not install
    `koalixcrm.accounting`."""

    id = models.BigAutoField(primary_key=True)
    tax_rate = models.DecimalField(max_digits=5,
                                   decimal_places=2,
                                   verbose_name=_("Taxrate in Percentage"))
    name = models.CharField(verbose_name=_("Taxname"),
                            max_length=100)

    def get_tax_rate(self):
        return self.tax_rate

    def clean(self):
        super().clean()
        if not apps.is_installed('koalixcrm.accounting'):
            return
        assignment = getattr(self, 'account_assignment', None)
        missing = []
        if assignment is None or assignment.activa_account_id is None:
            missing.append('activa_account')
        if assignment is None or assignment.passiva_account_id is None:
            missing.append('passiva_account')
        if missing:
            raise ValidationError(
                _(
                    "A TaxAccountAssignment with both activa and passiva accounts "
                    "is required when the accounting app is installed."
                )
            )

    def __str__(self):
        return self.name

    class Meta:
        app_label = "core"
        db_table = "crm_tax"
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')
