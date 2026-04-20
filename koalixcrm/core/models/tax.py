# -*- coding: utf-8 -*-

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _


class Tax(models.Model):
    id = models.BigAutoField(primary_key=True)
    tax_rate = models.DecimalField(max_digits=5,
                                   decimal_places=2,
                                   verbose_name=_("Taxrate in Percentage"))
    name = models.CharField(verbose_name=_("Taxname"),
                            max_length=100)
    account_activa = models.ForeignKey('accounting.Account',
                                       on_delete=models.CASCADE,
                                       verbose_name=_("Activa Account"),
                                       related_name="db_relaccountactiva",
                                       null=True,
                                       blank=True)
    account_passiva = models.ForeignKey('accounting.Account',
                                        on_delete=models.CASCADE,
                                        verbose_name=_("Passiva Account"),
                                        related_name="db_relaccountpassiva",
                                        null=True,
                                        blank=True)

    def get_tax_rate(self):
        return self.tax_rate

    def clean(self):
        super().clean()
        if apps.is_installed('koalixcrm.accounting'):
            missing = []
            if self.account_activa_id is None:
                missing.append('account_activa')
            if self.account_passiva_id is None:
                missing.append('account_passiva')
            if missing:
                raise ValidationError({
                    field: _("This field is required when the accounting app is installed.")
                    for field in missing
                })

    def __str__(self):
        return self.name

    class Meta:
        app_label = "core"
        db_table = "crm_tax"
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')
