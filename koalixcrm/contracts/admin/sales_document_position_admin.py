# -*- coding: utf-8 -*-

from django.contrib import admin
from koalixcrm.contracts.models.sales_document_position import SalesDocumentPosition


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
