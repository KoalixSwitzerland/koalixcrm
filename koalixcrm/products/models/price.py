# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.currency import Currency
from koalixcrm.core.models.currency_transform import CurrencyTransform
from koalixcrm.core.models.unit import Unit

# CustomerGroup referenced via string FK 'contacts.CustomerGroup'
from koalixcrm.core.models.unit_transform import UnitTransform
from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.models.customer_group_transform import CustomerGroupTransform


class Price(WorkspaceScopedModel):
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             blank=False,
                             verbose_name=_("Unit"))
    currency = models.ForeignKey(Currency,
                                 on_delete=models.CASCADE,
                                 verbose_name='Currency',
                                 blank=False,
                                 null=False)
    party_group = models.ForeignKey('contacts.PartyGroup',
                                    on_delete=models.PROTECT,
                                    related_name='prices',
                                    verbose_name=_("Party Group"),
                                    blank=True,
                                    null=True)
    price = models.DecimalField(max_digits=17,
                                decimal_places=2,
                                verbose_name=_("Price Per Unit"))
    valid_from = models.DateField(verbose_name=_("Valid from"),
                                  blank=True,
                                  null=True)
    valid_until = models.DateField(verbose_name=_("Valid until"),
                                   blank=True,
                                   null=True)

    def __str__(self):
        return str(self.id) + " " +str(self.price) + " " + str(self.currency.short_name)

    def is_valid_from_criteria_fulfilled(self, date):
        if self.valid_from is None:
            return True
        elif (self.valid_from - date).days <= 0:
            return True
        else:
            return False

    def is_valid_until_criteria_fulfilled(self, date):
        if self.valid_until is None:
            return True
        elif (date - self.valid_until).days <= 0:
            return True
        else:
            return False

    def is_party_group_criteria_fulfilled(self, party_group):
        if self.party_group is None:
            return True
        elif self.party_group == party_group:
            return True
        else:
            return False

    def is_currency_criteria_fulfilled(self, currency):
        if self.currency == currency:
            return True
        else:
            return False

    def is_unit_criteria_fulfilled(self, unit):
        if self.unit == unit:
            return True
        else:
            return False

    def is_date_in_range(self, date):
        if (self.valid_from is None) and (self.valid_until is None):
            return True
        elif self.valid_until is None:
            if self.valid_from <= date:
                return True
            else:
                return False
        elif self.valid_from is None:
            if date <= self.valid_until:
                return True
            else:
                return False
        elif (self.valid_from <= date) and (date <= self.valid_until):
            return True
        else:
            return False

    def get_currency_transform_factor(self, currency, product_type):
        """check currency conditions and factor"""
        currency_factor = 0
        if self.currency == currency:
            currency_factor = 1
        else:
            currency_transform = CurrencyTransform.objects.get(from_currency=self.currency,
                                                               to_currency=currency,
                                                               product_type=product_type)
            if currency_transform:
                currency_factor = currency_transform.get_transform_factor()
        return currency_factor

    def get_unit_transform_factor(self, unit, product_type):
        """check unit conditions and factor"""
        unit_factor = 0
        if self.unit == unit:
            unit_factor = 1
        else:
            unit_transform = UnitTransform.objects.get(from_unit=self.unit,
                                                       to_unit=unit,
                                                       product_type=product_type)
            if unit_transform:
                unit_factor = unit_transform.get_transform_factor()
        return unit_factor

    def get_party_group_transform_factor(self, party, product_type):
        """Search through all PartyGroup memberships the party belongs to.
        Return factor 1 for a perfect match, else the lowest transform factor.

        Args:
            party: koalixcrm.contacts.models.party.Party
            product_type: koalixcrm.products.models.product_type.ProductType

        Returns:
            Decimal factor
        """
        party_group_factor = 0
        if self.party_group is None:
            party_group_factor = 1
        elif party is not None:
            memberships = party.group_memberships.all()
            for membership in memberships:
                group = membership.party_group
                if self.party_group == group:
                    party_group_factor = 1
                    break
                else:
                    transform = CustomerGroupTransform.objects.filter(
                        from_party_group=self.party_group,
                        to_party_group=group,
                        product_type=product_type,
                    ).first()
                    if transform:
                        factor = transform.get_transform_factor()
                        if party_group_factor > factor or party_group_factor == 0:
                            party_group_factor = factor
        return party_group_factor

    class Meta:
        app_label = "products"
        db_table = "crm_price"
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')
