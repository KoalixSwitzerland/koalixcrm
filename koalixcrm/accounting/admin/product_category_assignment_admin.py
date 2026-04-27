# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import gettext as _

from koalixcrm.accounting.models.product_category_assignment import (
    ProductCategoryAssignment,
)


@admin.register(ProductCategoryAssignment)
class ProductCategoryAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_type', 'category')
    list_display_links = ('id',)
    search_fields = ('product_type__title', 'category__title')
    fieldsets = (
        (_('Basics'), {
            'fields': ('product_type', 'category'),
        }),
    )


class ProductCategoryAssignmentInline(admin.StackedInline):
    model = ProductCategoryAssignment
    extra = 0
    max_num = 1
    can_delete = True
    fieldsets = (
        (_('Accounting'), {
            'fields': ('category',),
        }),
    )
