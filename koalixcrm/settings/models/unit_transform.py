# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _


class UnitTransform(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_unit = models.ForeignKey('Unit',
                                  on_delete=models.CASCADE,
                                  verbose_name=_("From Unit"),
                                  blank=False,
                                  null=False,
                                  related_name="db_reltransfromfromunit")
    to_unit = models.ForeignKey('Unit',
                                on_delete=models.CASCADE,
                                verbose_name=_("To Unit"),
                                blank=False,
                                null=False,
                                related_name="db_reltransfromtounit")
    product_type = models.ForeignKey('products.ProductType',
                                     on_delete=models.CASCADE,
                                     blank=False,
                                     null=False,
                                     verbose_name=_("Product Type"))
    factor = models.DecimalField(verbose_name=_("Factor between From and To Unit"),
                                 blank=False,
                                 null=False,
                                 max_digits=17,
                                 decimal_places=2,)

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
        app_label = "settings"
        db_table = "crm_unittransform"
        verbose_name = _('Unit Transform')
        verbose_name_plural = _('Unit Transforms')
