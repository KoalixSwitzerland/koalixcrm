# -*- coding: utf-8 -*-

from decimal import Decimal
from koalixcrm.crm.documents.salesdocumentposition import SalesDocumentPosition
import koalixcrm.crm.documents.purchaseorder
import koalixcrm.crm.documents.salesdocument


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
            Can trow Product.NoPriceFound when Product Price could not be found"""

        price = 0
        tax = 0
        if isinstance(document, koalixcrm.crm.documents.salesdocument.SalesDocument):
            positions = SalesDocumentPosition.objects.filter(contract=document.id)
            contact_for_price_calculation = document.customer
            calculate_with_document_discount = True
        else:
            positions = koalixcrm.crm.documents.purchaseorder.PurchaseOrderPosition.objects.filter(contract=document.id)
            contact_for_price_calculation = document.supplier
            calculate_with_document_discount = False

        if positions.exists():
            for position in positions:
                price += Calculations.calculate_position_price(position, pricing_date, contact_for_price_calculation, document.currency)
                tax += Calculations.calculate_position_tax(position, document.currency)

            if calculate_with_document_discount:
                if isinstance(document.discount, Decimal):
                    price = int(price * (1 - document.discount / 100) / document.currency.rounding) * document.currency.rounding
                    tax = int(tax * (1 - document.discount / 100) / document.currency.rounding) * document.currency.rounding
        document.last_calculated_price = price
        document.last_calculated_tax = tax
        document.last_pricing_date = pricing_date
        document.save()
        return 1

    @staticmethod
    def calculate_position_price(position, pricing_date, contact, currency):
        """Performs a price calculation a position.
        The calculated price is stored in the last_calculated_price
        The date when the price was calculated is stored in last_pricing_date

        Args:
            position: possible document classes must be derived from Contract class
            pricing_date: must be a python date object
            contact: is used for the lookup of the correct price
            currency: is used for the lookup of the correct price and for the definition of the rounding

        Returns:
            calculated price
            or raises exception

        Raises:
            Can trow Product.NoPriceFound when Product Price could not be found"""

        if not position.overwrite_product_price:
            position.position_price_per_unit = position.product.get_price(pricing_date, position.unit, contact, currency)
        if isinstance(position.discount, Decimal):
            position.last_calculated_price = int(position.position_price_per_unit * position.quantity * (
                1 - position.discount / 100) / currency.rounding) * currency.rounding
        else:
            position.last_calculated_price = position.position_price_per_unit * position.quantity
        position.last_pricing_date = pricing_date
        position.save()
        return position.last_calculated_price

    @staticmethod
    def calculate_position_tax(position, currency):
        """Performs a tax calculation a position.
        The calculated tax is stored in the last_calculated_tax

        Args:
            position: possible document classes must be derived from Position class
            currency: is used for the definition of the rounding

        Returns:
            calculated tax
            or raises exception

        Raises:
            Can trow Product.NoPriceFound when Product Price could not be found"""
        if isinstance(position.discount, Decimal):
            position.last_calculated_tax = int(position.product.get_tax_rate() / 100 * position.position_price_per_unit * position.quantity * (
                1 - position.discount / 100) / currency.rounding) * currency.rounding
        else:
            position.last_calculated_tax = int(position.product.get_tax_rate() / 100 * position.position_price_per_unit * position.quantity /
                                             currency.rounding) * currency.rounding
        position.save()
        return position.last_calculated_tax
