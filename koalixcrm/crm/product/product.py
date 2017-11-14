# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from koalixcrm.crm.product.unit import UnitTransform
from koalixcrm.crm.contact.customergroup import CustomerGroup

import koalixcrm.crm.product.price


class Product(models.Model):
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    productNumber = models.IntegerField(verbose_name=_("Product Number"))
    defaultunit = models.ForeignKey("Unit", verbose_name=_("Unit"))
    dateofcreation = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    lastmodification = models.DateTimeField(verbose_name=_("Last modified"), auto_now=True)
    lastmodifiedby = models.ForeignKey('auth.User', limit_choices_to={'is_staff': True},
                                       verbose_name=_("Last modified by"), null=True, blank="True")
    tax = models.ForeignKey("Tax", blank=False)
    accoutingProductCategorie = models.ForeignKey('accounting.ProductCategorie',
                                                  verbose_name=_("Accounting Product Categorie"), null=True,
                                                  blank="True")

    def getPrice(self, date, unit, customer, currency):
        prices = koalixcrm.crm.product.price.Price.objects.filter(product=self.id)
        unitTransforms = UnitTransform.objects.filter(product=self.id)
        customerGroupTransforms = koalixcrm.crm.product.price.CustomerGroupTransform.objects.filter(product=self.id)
        validpriceslist = list()
        for price in list(prices):
            for customerGroup in CustomerGroup.objects.filter(customer=customer):
                if price.matchesDateUnitCustomerGroupCurrency(date, unit, customerGroup, currency):
                    validpriceslist.append(price.price);
                else:
                    for customerGroupTransform in customerGroupTransforms:
                        if price.matchesDateUnitCustomerGroupCurrency(date, unit,
                                                                      customerGroupTransfrom.transform(customerGroup),
                                                                      currency):
                            validpriceslist.append(price.price * customerGroup.factor);
                        else:
                            for unitTransfrom in list(unitTransforms):
                                if price.matchesDateUnitCustomerGroupCurrency(date,
                                                                              unitTransfrom.transfrom(unit).transform(
                                                                                      unitTransfrom),
                                                                              customerGroupTransfrom.transform(
                                                                                      customerGroup), currency):
                                    validpriceslist.append(
                                        price.price * customerGroupTransform.factor * unitTransform.factor);
        if (len(validpriceslist) > 0):
            lowestprice = validpriceslist[0]
            for price in validpriceslist:
                if (price < lowestprice):
                    lowestprice = price
            return lowestprice
        else:
            raise Product.NoPriceFound(customer, unit, date, currency, self)

    def getTaxRate(self):
        return self.tax.getTaxRate();

    def __str__(self):
        return str(self.productNumber) + ' ' + self.title

    class Meta:
        app_label = "crm"
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    class NoPriceFound(Exception):
        def __init__(self, customer, unit, date, currency, product):
            self.customer = customer
            self.unit = unit
            self.date = date
            self.product = product
            self.currency = currency
            return

        def __str__(self):
            return _("There is no Price for this product") + ": " + self.product.__str__() + _(
                "that matches the date") + ": " + self.date.__str__() + " ," + _(
                "customer") + ": " + self.customer.__str__() + " ," + _("currency")+ ": "+ self.currency.__str__()+ _(" and unit") + ":" + self.unit.__str__()

