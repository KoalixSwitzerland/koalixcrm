# -*- coding: utf-8 -*-
"""`Product` — the canonical catalog object (ADR-0003, ADR-0021).

Amendment 2026-06-27 renamed the former `ProductType` model (title, internal
number, unit, tax) to `Product`; the previous, semantically empty `Product`
identifier hull was removed in the same migration (0007) — its
identification role is carried by `ProductVariant` from here on
(ADR-0021 Korrektur 2).

Field keying per ADR-0021's authoritative table: `sku`, `gtin`, `mpn`,
`weight_kg`, `dimensions_*` live on `ProductVariant`, not here. `kind`,
`brand`, classification, `ServiceProfile`, `BillOfMaterials` and
`ProductPassport` anchor on `Product`.
"""
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.products.models.choices import KitMode, ProductKind, ProductLifecycleStatus
from koalixcrm.products.models.product_price import ProductPrice
from koalixcrm.products.services.product_lifecycle import validate_lifecycle_transition
from koalixcrm.products.services.product_kind_policy import validate_kind_change

if TYPE_CHECKING:
    from koalixcrm.contacts.models.party import Party
    from koalixcrm.core.models.currency import Currency
    from koalixcrm.core.models.unit import Unit


class Product(WorkspaceScopedModel):
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
    kind = models.CharField(verbose_name=_("Kind"),
                            max_length=32,
                            choices=ProductKind.choices)
    lifecycle_status = models.CharField(verbose_name=_("Lifecycle Status"),
                                        max_length=32,
                                        choices=ProductLifecycleStatus.choices,
                                        default=ProductLifecycleStatus.DRAFT)
    base_uom = models.ForeignKey("core.Unit", on_delete=models.CASCADE, verbose_name=_("Base Unit of Measure"))
    tax_class = models.ForeignKey("core.Tax",
                                  on_delete=models.CASCADE,
                                  verbose_name=_("Tax Class"),
                                  blank=False,
                                  null=False)
    brand = models.CharField(verbose_name=_("Brand"),
                             max_length=200,
                             null=True,
                             blank=True)
    manufacturer_party = models.ForeignKey("contacts.Party",
                                           on_delete=models.SET_NULL,
                                           verbose_name=_("Manufacturer"),
                                           related_name="manufactured_products",
                                           null=True,
                                           blank=True)
    country_of_origin = models.CharField(verbose_name=_("Country of Origin"),
                                         max_length=2,
                                         null=True,
                                         blank=True,
                                         help_text=_("ISO 3166-1 alpha-2 country code."))
    product_family = models.ForeignKey("ProductFamily",
                                       on_delete=models.SET_NULL,
                                       verbose_name=_("Product Family"),
                                       related_name="products",
                                       null=True,
                                       blank=True)
    kit_mode = models.CharField(verbose_name=_("Kit Mode"),
                                max_length=16,
                                choices=KitMode.choices,
                                default=KitMode.EXPLODE_ON_PICK,
                                help_text=_("ADR-0014: only evaluated by the application layer "
                                            "for kind = KIT."))
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

    def clean(self) -> None:
        super().clean()
        old_status = None
        old_kind = None
        if self.pk is not None:
            old_row = (
                Product.objects.filter(pk=self.pk)
                .values_list("lifecycle_status", "kind")
                .first()
            )
            if old_row is not None:
                old_status, old_kind = old_row
        validate_lifecycle_transition(old_status, self.lifecycle_status)
        # ADR-0019: kind is immutable once a lock-set member exists.
        validate_kind_change(self, old_kind, self.kind)

    def get_price(
        self,
        date: datetime.date,
        unit: Unit,
        party: Party | None,
        currency: Currency,
    ) -> Decimal:
        """Find the applicable price for this Product at `date` for the
        given `party`, returning the price as a Decimal.

        Args:
            party: koalixcrm.contacts.models.party.Party  (the customer)
            unit: koalixcrm.core.models.Unit
            currency: koalixcrm.core.models.Currency
            date: datetime.date

        Raises:
            NoPriceFound if no valid product price matches.
        """
        # ADR-0021 Amendment 2026-06-28: ProductPrice keys to ProductVariant,
        # not Product. This Product-level lookup considers prices across all
        # of this Product's variants (a superset of the pre-rekey behaviour,
        # which is identical for the common single-variant case). Callers
        # that need a specific variant's price should query
        # `ProductPrice.objects.filter(variant=variant)` or use
        # `koalixcrm.products.services.price_resolution.resolve_price`
        # directly.
        prices = ProductPrice.objects.filter(variant__product=self)
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
            raise Product.NoPriceFound(party, unit, date, currency, self)

    def get_tax_rate(self) -> Decimal:
        return self.tax_class.get_tax_rate()

    def __str__(self) -> str:
        return str(self.product_type_identifier) + ' ' + self.title.__str__()

    class Meta:
        app_label = "products"
        db_table = "products_product"
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    class NoPriceFound(Exception):
        def __init__(
            self,
            party: Party | None,
            unit: Unit,
            date: datetime.date,
            currency: Currency,
            product: Product,
        ) -> None:
            self.party = party
            self.unit = unit
            self.date = date
            self.product = product
            self.currency = currency

        def __str__(self) -> str:
            return _("There is no Price for this product") + ": " + self.product.__str__() + _(
                "that matches the date") + ": " + self.date.__str__() + " ," + _(
                "party") + ": " + self.party.__str__() + " ," + _(
                "currency") + ": " + self.currency.__str__() + _(" and unit") + ":" + self.unit.__str__()
