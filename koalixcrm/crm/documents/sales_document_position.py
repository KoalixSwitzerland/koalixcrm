# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.utils.translation import gettext as _


class Position(models.Model):
    id = models.BigAutoField(primary_key=True)
    position_number = models.PositiveIntegerField(verbose_name=_("Position Number"),
                                                  validators=[MinValueValidator(1)])
    quantity = models.DecimalField(verbose_name=_("Quantity"),
                                   decimal_places=3,
                                   max_digits=10)
    description = models.TextField(verbose_name=_("Description"),
                                   blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2,
                                   verbose_name=_("Discount"),
                                   blank=True,
                                   null=True)
    product_type = models.ForeignKey("ProductType",
                                     on_delete=models.CASCADE,
                                     verbose_name=_("Product"),
                                     blank=False,
                                     null=True)
    unit = models.ForeignKey("Unit",
                             on_delete=models.CASCADE,
                             verbose_name=_("Unit"),
                             blank=True,
                             null=True)
    sent_on = models.DateField(verbose_name=_("Shipment on"),
                               blank=True,
                               null=True)
    overwrite_product_price = models.BooleanField(verbose_name=_('Overwrite Product Price'))
    position_price_per_unit = models.DecimalField(verbose_name=_("Price Per Unit"),
                                                  max_digits=17,
                                                  decimal_places=2,
                                                  blank=True, null=True)
    last_pricing_date = models.DateField(verbose_name=_("Last Pricing Date"),
                                         blank=True,
                                         null=True)
    last_calculated_price = models.DecimalField(max_digits=17,
                                                decimal_places=2,
                                                verbose_name=_("Last Calculated Price"),
                                                blank=True, null=True)
    last_calculated_tax = models.DecimalField(max_digits=17,
                                              decimal_places=2,
                                              verbose_name=_("Last Calculated Tax"),
                                              blank=True,
                                              null=True)

    def __str__(self):
        return _("Position") + ": " + self.id.__str__()

    class Meta:
        app_label = "crm"
        ordering = ["position_number"]
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')


class SalesDocumentPosition(Position):
    sales_document = models.ForeignKey("SalesDocument", on_delete=models.CASCADE, verbose_name=_("Contract"))

    class Meta:
        app_label = "crm"
        verbose_name = _('Position in Sales Document')
        verbose_name_plural = _('Positions Sales Document')

    @staticmethod
    def add_positions(position_class, object_to_create_pdf):
        from koalixcrm.crm.product.unit import Unit
        from koalixcrm.crm.product.product_type import ProductType
        objects = list(position_class.objects.filter(sales_document=object_to_create_pdf.id))
        for position in list(position_class.objects.filter(sales_document=object_to_create_pdf.id)):
            objects += list(Position.objects.filter(id=position.id))
            objects += list(ProductType.objects.filter(id=position.product_type.id))
            objects += list(Unit.objects.filter(id=position.unit.id))
        return objects

    def create_position(self, calling_model, attach_to_model):
        """Copies all the content of the calling model and attaches
        links itself to the attach_to_model, this function is usually
        used within the create invoice, quote, reminder,... functions"""

        self.product_type = calling_model.product_type
        self.position_number = calling_model.position_number
        self.quantity = calling_model.quantity
        self.description = calling_model.description
        self.discount = calling_model.discount
        self.unit = calling_model.unit
        self.sent_on = calling_model.sent_on
        self.overwrite_product_price = calling_model.overwrite_product_price
        self.position_price_per_unit = calling_model.position_price_per_unit
        self.last_pricing_date = calling_model.last_pricing_date
        self.last_calculated_price = calling_model.last_calculated_price
        self.last_calculated_tax = calling_model.last_calculated_tax
        self.sales_document = attach_to_model
        self.save()

    def __str__(self):
        return _("Sales Document Position") + ": " + str(self.id)

    class NoPriceFound(Exception):
        def __str__(self):
            return _("There is no Price set for the sales document position")


class SalesDocumentInlinePosition(admin.TabularInline):
    model = SalesDocumentPosition
    extra = 1
    classes = ['expand']
    fieldsets = (
        ('', {
            'fields': (
                'position_number',
                'quantity',
                'unit',
                'product_type',
                'description',
                'discount',
                'overwrite_product_price',
                'position_price_per_unit',
                'sent_on')
        }),
    )
    allow_add = True

