# -*- coding: utf-8 -*-
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from koalixcrm.core.models.unit import Unit
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

    def transform(self, unit: 'Unit') -> 'Unit | None':
        if self.from_unit == unit:
            return self.to_unit
        else:
            return None

    def get_transform_factor(self) -> Decimal:
        return self.factor

    def __str__(self) -> str:
        return "From " + self.from_unit.short_name + " to " + self.to_unit.short_name

    class Meta:
        app_label = "core"
        db_table = "crm_unittransform"
        verbose_name = _('Unit Transform')
        verbose_name_plural = _('Unit Transforms')
