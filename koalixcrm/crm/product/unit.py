# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class Unit(models.Model):
    description = models.CharField(verbose_name=_("Description"), max_length=100)
    short_name = models.CharField(verbose_name=_("Displayed Name After Quantity In The Position"), max_length=3)
    is_a_fraction_of = models.ForeignKey('self', blank=True, null=True, verbose_name=_("Is A Fraction Of"))
    fraction_factor_to_next_higher_unit = models.IntegerField(verbose_name=_("Factor Between This And Next Higher Unit"),
                                                              blank=True, null=True)

    def __str__(self):
        return self.short_name

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')


class UnitTransform(models.Model):
    from_unit = models.ForeignKey('Unit', verbose_name=_("From Unit"), related_name="db_reltransfromfromunit")
    to_unit = models.ForeignKey('Unit', verbose_name=_("To Unit"), related_name="db_reltransfromtounit")
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Unit"), blank=True, null=True)

    def transform(self, unit):
        if (self.from_unit == unit):
            return self.to_unit
        else:
            return unit

    def __str__(self):
        return "From " + self.from_unit.short_name + " to " + self.to_unit.short_name

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit Transfrom')
        verbose_name_plural = _('Unit Transfroms')