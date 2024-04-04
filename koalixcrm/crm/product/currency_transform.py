# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _


class CurrencyTransform(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_currency = models.ForeignKey('Currency',
                                      on_delete=models.CASCADE,
                                      blank=False,
                                      null=False,
                                      verbose_name=_("From Currency"),
                                      related_name="db_reltransformfromcurrency")
    to_currency = models.ForeignKey('Currency',
                                    on_delete=models.CASCADE,
                                    blank=False,
                                    null=False,
                                    verbose_name=_("To Currency"),
                                    related_name="db_reltransformtocurrency")
    product_type = models.ForeignKey('ProductType',
                                     on_delete=models.CASCADE,
                                     blank=False,
                                     null=False,
                                     verbose_name=_("Product"))
    factor = models.DecimalField(verbose_name=_("Factor between From and To Currency"),
                                 blank=False,
                                 null=False,
                                 max_digits=17,
                                 decimal_places=2,)

    def get_transform_factor(self):
        return self.factor

    def __str__(self):
        return "From " + self.from_currency.short_name + " to " + self.to_currency.short_name

    class Meta:
        app_label = "crm"
        verbose_name = _('Currency Transform')
        verbose_name_plural = _('Currency Transforms')


class CurrencyTransformInlineAdminView(admin.TabularInline):
    model = CurrencyTransform
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('from_currency',
                       'to_currency',
                       'factor',)
        }),
    )
    allow_add = True
