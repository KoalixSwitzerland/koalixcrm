# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class CustomerGroupTransform(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    from_party_group = models.ForeignKey('contacts.PartyGroup',
                                         on_delete=models.PROTECT,
                                         related_name='transforms_from',
                                         verbose_name=_("From Party Group"))
    to_party_group = models.ForeignKey('contacts.PartyGroup',
                                       on_delete=models.PROTECT,
                                       related_name='transforms_to',
                                       verbose_name=_("To Party Group"))
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

    def transform(self, party_group):
        """Return `to_party_group` if the given party_group matches this
        transform's `from_party_group`, else None."""
        if self.from_party_group == party_group:
            return self.to_party_group
        return None

    def get_transform_factor(self):
        return self.factor

    def __str__(self):
        return "From " + self.from_party_group.name + " to " + self.to_party_group.name

    class Meta:
        app_label = "products"
        db_table = "crm_customergrouptransform"
        verbose_name = _('Customer Group Price Transform')
        verbose_name_plural = _('Customer Group Price Transforms')
