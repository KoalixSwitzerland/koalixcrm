# -*- coding: utf-8 -*-

from decimal import Decimal
import koalixcrm.crm.documents.salescontractposition
import koalixcrm.crm.documents.purchaseorder
import koalixcrm.crm.documents.quote
import koalixcrm.crm.documents.invoice


class Calculations:

    @staticmethod
    def calculate_document_price(document, pricing_date):
        """Performs a price recalculation on contact documents.
        The calculated price is stored in the lastCalculatedPrice and lastCalculatedTax.
        The date when the price was calculated is stored in lastPricingDate

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
        if (type(document) == koalixcrm.crm.documents.quote.Quote) or \
                (type(document) == koalixcrm.crm.documents.invoice.Invoice):
            positions = koalixcrm.crm.documents.salescontractposition.SalesContractPosition.objects.filter(contract=document.id)
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
        document.lastCalculatedPrice = price
        document.lastCalculatedTax = tax
        document.lastPricingDate = pricing_date
        document.save()
        return 1

    @staticmethod
    def calculate_position_price(position, pricing_date, contact, currency):
        """Performs a price calculation a position.
        The calculated price is stored in the lastCalculatedPrice
        The date when the price was calculated is stored in lastPricingDate

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

        if not position.overwriteProductPrice:
            position.positionPricePerUnit = position.product.getPrice(pricing_date, position.unit, contact, currency)
        if isinstance(position.discount, Decimal):
            position.lastCalculatedPrice = int(position.positionPricePerUnit * position.quantity * (
                1 - position.discount / 100) / currency.rounding) * currency.rounding
        else:
            position.lastCalculatedPrice = position.positionPricePerUnit * position.quantity
        position.lastPricingDate = pricing_date
        position.save()
        return position.lastCalculatedPrice

    @staticmethod
    def calculate_position_tax(position, currency):
        """Performs a tax calculation a position.
        The calculated tax is stored in the lastCalculatedPrice

        Args:
            position: possible document classes must be derived from Position class
            currency: is used for the definition of the rounding

        Returns:
            calculated tax
            or raises exception

        Raises:
            Can trow Product.NoPriceFound when Product Price could not be found"""
        if isinstance(position.discount, Decimal):
            position.lastCalculatedTax = int(position.product.getTaxRate() / 100 * position.positionPricePerUnit * position.quantity * (
                1 - position.discount / 100) / currency.rounding) * currency.rounding
        else:
            position.lastCalculatedTax = int(position.product.getTaxRate() / 100 * position.positionPricePerUnit * position.quantity /
                                             currency.rounding) * currency.rounding
        position.save()
        return position.lastCalculatedTax
