# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
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
        return self.tax_rate;

    def __str__(self):
        return self.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Tax')
        verbose_name_plural = _('Taxes')


class OptionTax(admin.ModelAdmin):
    list_display = ('id',
                    'tax_rate',
                    'name',
                    'account_activa',
                    'account_passiva')
    fieldsets = (('', {'fields': ('tax_rate',
                                  'name',
                                  'account_activa',
                                  'account_passiva')}),)
    allow_add = True


