# -*- coding: utf-8 -*-

from decimal import Decimal
from koalixcrm.contracts.models.commercial_document_position import CommercialDocumentPosition


class Calculations:

    @staticmethod
    def calculate_document_price(document, pricing_date):
        """Performs a price recalculation on contact documents.
        The calculated price is stored in the last_calculated_price and last_calculated_tax.
        The date when the price was calculated is stored in last_pricing_date

        Args:
            document: possible document classes must be derived from Contract
            pricing_date: must be a python date object

        Returns:
            1 (Boolean) when passed
            or raises exception

        Raises:
            Can trow Product.NoPriceFound when Product Price was overwritten but the price was not set
            Can trow Position.NoPriceFound when Position Price has no value but overwrite price is set """

        price = 0
        tax = 0
        positions = CommercialDocumentPosition.objects.filter(commercial_document=document.id)
        party_for_price_calculation = document.party
        if positions.exists():
            for position in positions:
                price += Calculations.calculate_position_price(position,
                                                               pricing_date,
                                                               party_for_price_calculation,
                                                               document.currency)
                tax += Calculations.calculate_position_tax(position, document.currency)
            if document.discount is not None:
                discount = Decimal(document.discount)
                total_price = price * (1 - discount / 100)
                total_tax = tax * (1 - discount / 100)
                total_price = Decimal(total_price)
                total_tax = Decimal(total_tax)
                price = document.currency.round(total_price)
                tax = document.currency.round(total_tax)
            else:
                tax = document.currency.round(tax)
                price = document.currency.round(price)
        document.last_calculated_price = price
        document.last_calculated_tax = tax
        document.last_pricing_date = pricing_date
        document.save()
        return 1

    @staticmethod
    def calculate_position_price(position, pricing_date, party, currency):
        """Compute the position price. Requires either (a) a product type that
        can answer `get_price(...)`, or (b) `overwrite_product_price=True` with
        `position_price_per_unit` set. The second shape is also used when the
        `products` app is not installed."""

        if position.product_type_id is None or position.overwrite_product_price:
            if position.position_price_per_unit is None:
                raise CommercialDocumentPosition.NoPriceFound
        else:
            position.position_price_per_unit = position.product_type.get_price(
                pricing_date, position.unit, party, currency
            )
        nominal_total = position.position_price_per_unit * position.quantity
        if isinstance(position.discount, Decimal):
            nominal_minus_discount = nominal_total * (1 - position.discount / 100)
        else:
            nominal_minus_discount = nominal_total
        total_with_tax = Decimal(nominal_minus_discount)
        position.last_calculated_price = total_with_tax
        position.last_pricing_date = pricing_date
        position.save()
        return position.last_calculated_price

    @staticmethod
    def calculate_position_tax(position, currency):
        """Compute position tax. Tax rate source order:
        1. `position.product_type.get_tax_rate()` if a product type is linked.
        2. `position.position_tax_rate` as position-local fallback.
        3. Zero otherwise."""
        nominal_total = position.position_price_per_unit * position.quantity
        if isinstance(position.discount, Decimal):
            nominal_minus_discount = nominal_total * (1 - position.discount / 100)
        else:
            nominal_minus_discount = nominal_total
        if position.product_type_id is not None:
            tax_rate = position.product_type.get_tax_rate()
        elif position.position_tax_rate is not None:
            tax_rate = position.position_tax_rate
        else:
            tax_rate = Decimal(0)
        total_tax = nominal_minus_discount * Decimal(tax_rate) / 100
        total_tax = Decimal(total_tax)
        position.last_calculated_tax = total_tax
        position.save()
        return position.last_calculated_tax
