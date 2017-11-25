from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext as _


class Position(models.Model):
    positionNumber = models.IntegerField(verbose_name=_("Position Number"))
    quantity = models.DecimalField(verbose_name=_("Quantity"), decimal_places=3, max_digits=10)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount"), blank=True, null=True)
    product = models.ForeignKey("Product", verbose_name=_("Product"), blank=True, null=True)
    unit = models.ForeignKey("Unit", verbose_name=_("Unit"), blank=True, null=True)
    sentOn = models.DateField(verbose_name=_("Shipment on"), blank=True, null=True)
    overwriteProductPrice = models.BooleanField(verbose_name=_('Overwrite Product Price'))
    positionPricePerUnit = models.DecimalField(verbose_name=_("Price Per Unit"), max_digits=17, decimal_places=2,
                                               blank=True, null=True)
    lastPricingDate = models.DateField(verbose_name=_("Last Pricing Date"), blank=True, null=True)
    lastCalculatedPrice = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Price"),
                                              blank=True, null=True)
    lastCalculatedTax = models.DecimalField(max_digits=17, decimal_places=2, verbose_name=_("Last Calculted Tax"),
                                            blank=True, null=True)

    def __str__(self):
        return _("Position") + ": " + str(self.id)

    class Meta:
        app_label = "crm"
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')


class SalesContractPosition(Position):
    contract = models.ForeignKey("SalesContract", verbose_name=_("Contract"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Salescontract Position')
        verbose_name_plural = _('Salescontract Positions')

    def __str__(self):
        return _("Salescontract Position") + ": " + str(self.id)


