# -*- coding: utf-8 -*-

from decimal import Decimal
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _


class Currency(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(verbose_name=_("Description"),
                                   max_length=100)
    short_name = models.CharField(verbose_name=_("Displayed Name After Prices"),
                                  max_length=3)
    rounding = models.DecimalField(max_digits=5,
                                   decimal_places=2,
                                   verbose_name=_("Rounding"),
                                   blank=True,
                                   null=True)

    def get_rounding(self):
        """Returns either the stored rounding value for a currency or a default rounding value of 0.05

        Args: no arguments

        Returns: Decimal value

        Raises: should not return exceptions"""
        if self.rounding is None:
            return Decimal('0.05')
        else:
            return self.rounding

    def round(self, value):
        """Rounds the input value to the rounding resolution which is defined in the variable "rounding"

        Args: Decimal value value

        Returns: Decimal value

        Raises: should not return exceptions"""
        rounded_value = int(value / self.get_rounding()) * self.get_rounding()
        return rounded_value

    def __str__(self):
        return self.short_name

    class Meta:
        app_label = "crm"
        verbose_name = _('Currency')
        verbose_name_plural = _('Currency')


class OptionCurrency(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'short_name',
                    'rounding')
    fieldsets = (('', {'fields': ('description',
                                  'short_name',
                                  'rounding')}),)
    allow_add = True
