# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _


class Unit(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(verbose_name=_("Description"),
                                   max_length=100)
    short_name = models.CharField(verbose_name=_("Displayed Name After Quantity In The Position"),
                                  max_length=3)
    is_a_fraction_of = models.ForeignKey('self',
                                         on_delete=models.CASCADE,
                                         blank=True,
                                         null=True,
                                         verbose_name=_("Is A Fraction Of"))
    fraction_factor_to_next_higher_unit = models.DecimalField(verbose_name=_("Factor Between This And Next Higher Unit"),
                                                              max_digits=20,
                                                              decimal_places=10,
                                                              blank=True,
                                                              null=True)

    def __str__(self):
        return self.short_name

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')


class OptionUnit(admin.ModelAdmin):
    list_display = ('id',
                    'description',
                    'short_name',
                    'is_a_fraction_of',
                    'fraction_factor_to_next_higher_unit')
    fieldsets = (('', {'fields': ('description',
                                  'short_name',
                                  'is_a_fraction_of',
                                  'fraction_factor_to_next_higher_unit')}),)
    allow_add = True

