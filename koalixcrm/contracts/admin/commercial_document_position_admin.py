# -*- coding: utf-8 -*-

from django.apps import apps
from django.contrib import admin

from koalixcrm.contracts.models.commercial_document_position import (
    CommercialDocumentPosition,
)


def _position_fields() -> tuple[str, ...]:
    base: list[str] = [
        'position_number',
        'quantity',
        'unit',
    ]
    if apps.is_installed('koalixcrm.products'):
        base.append('product_type')
    base += [
        'description',
        'discount',
        'overwrite_product_price',
        'position_price_per_unit',
        'position_tax_rate',
        'sent_on',
    ]
    return tuple(base)


class CommercialDocumentInlinePosition(admin.TabularInline):
    model = CommercialDocumentPosition
    extra = 1
    classes = ['expand']
    fieldsets = (
        ('', {
            'fields': _position_fields(),
        }),
    )
    allow_add = True
