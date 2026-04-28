# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.models.product_price import ProductPrice

if TYPE_CHECKING:
    from koalixcrm.contacts.models.party import Party
    from koalixcrm.core.models.currency import Currency
    from koalixcrm.core.models.unit import Unit


class ProductType(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField(verbose_name=_("Description"),
                                   null=True,
                                   blank=True)
    title = models.CharField(verbose_name=_("Title"),
                             max_length=200)
    product_type_identifier = models.CharField(verbose_name=_("Product Number"),
                                               max_length=200,
                                               null=True,
                                               blank=True)
    default_unit = models.ForeignKey("core.Unit", on_delete=models.CASCADE, verbose_name=_("Unit"))
    tax = models.ForeignKey("core.Tax",
                            on_delete=models.CASCADE,
                            blank=False,
                            null=False)
    last_modification = models.DateTimeField(verbose_name=_("Last modified"),
                                             auto_now=True)
    last_modified_by = models.ForeignKey('auth.User',
                                         on_delete=models.CASCADE,
                                         limit_choices_to={'is_staff': True},
                                         verbose_name=_("Last modified by"),
                                         null=True,
                                         blank=True)
    date_of_creation = models.DateTimeField(verbose_name=_("Created at"),
                                            auto_now_add=True)

    def get_price(
        self,
        date: datetime.date,
        unit: Unit,
        party: Party | None,
        currency: Currency,
    ) -> Decimal:
        """Find the applicable price for this ProductType at `date` for the
        given `party`, returning the price as a Decimal.

        Args:
            party: koalixcrm.contacts.models.party.Party  (the customer)
            unit: koalixcrm.core.models.Unit
            currency: koalixcrm.core.models.Currency
            date: datetime.date

        Raises:
            NoPriceFound if no valid product price matches.
        """
        prices = ProductPrice.objects.filter(product_type=self)
        valid_prices = list()
        for price in list(prices):
            currency_factor = price.get_currency_transform_factor(currency, self.id)
            unit_factor = price.get_unit_transform_factor(unit, self.id)
            group_factor = price.get_party_group_transform_factor(party, self.id)
            date_in_range = price.is_date_in_range(date)
            if date_in_range \
                    and currency_factor != 0 \
                    and unit_factor != 0 \
                    and group_factor != 0:
                transformed_price = price.price*group_factor*unit_factor*currency_factor
                valid_prices.append(transformed_price)
        if len(valid_prices) > 0:
            lowest_price = valid_prices[0]
            for price in valid_prices:
                if price < lowest_price:
                    lowest_price = price
            return lowest_price
        else:
            raise ProductType.NoPriceFound(party, unit, date, currency, self)

    def get_tax_rate(self) -> Decimal:
        return self.tax.get_tax_rate()

    def __str__(self) -> str:
        return str(self.product_type_identifier) + ' ' + self.title.__str__()

    class Meta:
        app_label = "products"
        db_table = "crm_producttype"
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')

    class NoPriceFound(Exception):
        def __init__(
            self,
            party: Party | None,
            unit: Unit,
            date: datetime.date,
            currency: Currency,
            product: ProductType,
        ) -> None:
            self.party = party
            self.unit = unit
            self.date = date
            self.product = product
            self.currency = currency

        def __str__(self) -> str:
            return _("There is no Price for this product type") + ": " + self.product.__str__() + _(
                "that matches the date") + ": " + self.date.__str__() + " ," + _(
                "party") + ": " + self.party.__str__() + " ," + _(
                "currency") + ": " + self.currency.__str__() + _(" and unit") + ":" + self.unit.__str__()
