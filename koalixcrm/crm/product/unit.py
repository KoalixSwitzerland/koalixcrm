# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class Unit(models.Model):
    description = models.CharField(verbose_name=_("Description"), max_length=100)
    shortName = models.CharField(verbose_name=_("Displayed Name After Quantity In The Position"), max_length=3)
    isAFractionOf = models.ForeignKey('self', blank=True, null=True, verbose_name=_("Is A Fraction Of"))
    fractionFactorToNextHigherUnit = models.IntegerField(verbose_name=_("Factor Between This And Next Higher Unit"),
                                                         blank=True, null=True)

    def __str__(self):
        return self.shortName

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')


class UnitTransform(models.Model):
    fromUnit = models.ForeignKey('Unit', verbose_name=_("From Unit"), related_name="db_reltransfromfromunit")
    toUnit = models.ForeignKey('Unit', verbose_name=_("To Unit"), related_name="db_reltransfromtounit")
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Unit"), blank=True, null=True)

    def transform(self, unit):
        if (self.fromUnit == unit):
            return self.toUnit
        else:
            return unit

    def __str__(self):
        return "From " + self.fromUnit.shortName + " to " + self.toUnit.shortName

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit Transfrom')
        verbose_name_plural = _('Unit Transfroms')