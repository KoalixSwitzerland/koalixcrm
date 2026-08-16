# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class Position(models.Model):
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
    product_type = models.ForeignKey("products.Product",
                                     on_delete=models.CASCADE,
                                     verbose_name=_("Product"),
                                     blank=True,
                                     null=True)
    unit = models.ForeignKey("core.Unit",
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
    position_tax_rate = models.DecimalField(verbose_name=_("Tax Rate (%)"),
                                            max_digits=5,
                                            decimal_places=2,
                                            blank=True,
                                            null=True,
                                            help_text=_(
                                                "Used for tax calculation when no "
                                                "product type is set on the position."
                                            ))
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

    def clean(self) -> None:
        super().clean()
        if self.product_type_id is None:
            errors: dict[str, Any] = {}
            if not self.overwrite_product_price:
                errors['overwrite_product_price'] = _(
                    "Required when no product type is set on the position."
                )
            if self.position_price_per_unit is None:
                errors['position_price_per_unit'] = _(
                    "Required when no product type is set on the position."
                )
            if errors:
                raise ValidationError(errors)
        elif not apps.is_installed('koalixcrm.products'):
            raise ValidationError({
                'product_type': _(
                    "Cannot reference a product type: the products app is not installed."
                ),
            })

    def __str__(self) -> str:
        return _("Position") + ": " + str(self.id)

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_position"
        ordering = ["position_number"]
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')


class CommercialDocumentPosition(WorkspaceScopedModel, Position):
    commercial_document = models.ForeignKey("CommercialDocument", on_delete=models.CASCADE, verbose_name=_("Contract"))

    class Meta:
        app_label = "contract_object_management"
        db_table = "crm_commercialdocumentposition"
        verbose_name = _('Position in Commercial Document')
        verbose_name_plural = _('Positions Commercial Document')

    @staticmethod
    def add_positions(position_class: type[models.Model], object_to_create_pdf: models.Model) -> list[models.Model]:
        from koalixcrm.core.models.unit import Unit
        product_type_model: type[models.Model] | None = None
        if apps.is_installed('koalixcrm.products'):
            product_type_model = apps.get_model('products', 'Product')
        objects = list(position_class.objects.filter(commercial_document=object_to_create_pdf.id))
        for position in list(position_class.objects.filter(commercial_document=object_to_create_pdf.id)):
            objects += list(Position.objects.filter(id=position.id))
            if product_type_model is not None and position.product_type_id is not None:
                objects += list(product_type_model.objects.filter(id=position.product_type_id))
            if position.unit_id is not None:
                objects += list(Unit.objects.filter(id=position.unit_id))
        return objects

    def create_position(self, calling_model: Position, attach_to_model: models.Model) -> None:
        """Copies all the content of the calling model and attaches
        links itself to the attach_to_model, this function is usually
        used within the create invoice, quotation, reminder,... functions"""

        self.product_type = calling_model.product_type
        self.position_number = calling_model.position_number
        self.quantity = calling_model.quantity
        self.description = calling_model.description
        self.discount = calling_model.discount
        self.unit = calling_model.unit
        self.sent_on = calling_model.sent_on
        self.overwrite_product_price = calling_model.overwrite_product_price
        self.position_price_per_unit = calling_model.position_price_per_unit
        self.position_tax_rate = calling_model.position_tax_rate
        self.last_pricing_date = calling_model.last_pricing_date
        self.last_calculated_price = calling_model.last_calculated_price
        self.last_calculated_tax = calling_model.last_calculated_tax
        self.commercial_document = attach_to_model
        self.save()

    def __str__(self) -> str:
        return _("Commercial Document Position") + ": " + str(self.id)

    class NoPriceFound(Exception):
        def __str__(self) -> str:
            return _("There is no Price set for the commercial document position")
