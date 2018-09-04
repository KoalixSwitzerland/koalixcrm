# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext as _


class UnitTransform(models.Model):
    from_unit = models.ForeignKey('Unit',
                                  verbose_name=_("From Unit"),
                                  related_name="db_reltransfromfromunit")
    to_unit = models.ForeignKey('Unit',
                                verbose_name=_("To Unit"),
                                related_name="db_reltransfromtounit")
    product = models.ForeignKey('Product',
                                verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Unit"),
                                 blank=True,
                                 null=True)

    def transform(self, unit):
        if self.from_unit == unit:
            return self.to_unit
        else:
            return None

    def get_transform_factor(self):
        return self.factor

    def __str__(self):
        return "From " + self.from_unit.short_name + " to " + self.to_unit.short_name

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit Transform')
        verbose_name_plural = _('Unit Transforms')


class ProductUnitTransform(admin.TabularInline):
    model = UnitTransform
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('from_unit',
                       'to_unit',
                       'factor',)
        }),
    )
    allow_add = True
