# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext as _


class CustomerGroupTransform(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_customer_group = models.ForeignKey('CustomerGroup',
                                            on_delete=models.CASCADE,
                                            verbose_name=_("From Customer Group"),
                                            related_name="db_reltransfromfromcustomergroup",
                                            blank=False,
                                            null=False)
    to_customer_group = models.ForeignKey('CustomerGroup',
                                          on_delete=models.CASCADE,
                                          verbose_name=_("To Customer Group"),
                                          related_name="db_reltransfromtocustomergroup",
                                          blank=False,
                                          null=False)
    product_type = models.ForeignKey('ProductType',
                                     on_delete=models.CASCADE,
                                     verbose_name=_("Product Type"),
                                     blank=False,
                                     null=False)
    factor = models.DecimalField(verbose_name=_("Factor between From and To Customer Group"),
                                 blank=False,
                                 null=False,
                                 max_digits=17,
                                 decimal_places=2,)

    def transform(self, customer_group):
        """The transform function verifies whether the provided argument customer_group
        is corresponding with the "from_customer_group" variable of the CustomerGroupTransform class
        When this is ok, the function returns the "to_customer_group". When the provided customer_group
        argument is not corresponding, the function returns a "None"

        Args:
        customer_group: CustomerGroup object

        Returns:
        CustomerGroup object or None

        Raises:
        No exceptions planned"""
        if self.from_customer_group == customer_group:
            return self.to_customer_group
        else:
            return None

    def get_transform_factor(self):
        return self.factor

    def __str__(self):
        return "From " + self.from_customer_group.name + " to " + self.to_customer_group.name

    class Meta:
        app_label = "crm"
        verbose_name = _('Customer Group Price Transform')
        verbose_name_plural = _('Customer Group Price Transforms')


class CustomerGroupTransformInlineAdminView(admin.TabularInline):
    model = CustomerGroupTransform
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('from_customer_group',
                       'to_customer_group',
                       'factor',)
        }),
    )
    allow_add = True
