# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class Tax(models.Model):
    taxrate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Taxrate in Percentage"))
    name = models.CharField(verbose_name=_("Taxname"), max_length=100)
    accountActiva = models.ForeignKey('accounting.Account', verbose_name=_("Activa Account"),
                                      related_name="db_relaccountactiva", null=True, blank=True)
    accountPassiva = models.ForeignKey('accounting.Account', verbose_name=_("Passiva Account"),
                                       related_name="db_relaccountpassiva", null=True, blank=True)

    def getTaxRate(self):
        return self.taxrate;

    def __str__(self):
        return self.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')