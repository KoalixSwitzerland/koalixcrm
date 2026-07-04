# -*- coding: utf-8 -*-
"""ProductionOrderAdmin for koalixcrm stock (ADR-0014). Admin actions route
`release`/`start`/`complete`/`cancel` through
`services/production_order_workflow.py`. `complete` needs a
`destination_location` and `finished_variant` per order — since bulk
completion can't collect per-row parameters through a plain admin action,
`action_complete` uses each order's product's first variant and its
`components`' reservation location as a best-effort default; operators
needing precise control should use the REST `complete` action instead."""
from __future__ import annotations

from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.production_order import ProductionOrder
from koalixcrm.stock.models.production_order_component import ProductionOrderComponent
from koalixcrm.stock.services import production_order_workflow
from koalixcrm.stock.services.bom_explosion import ExplosionDepthExceeded, explode


class ProductionOrderComponentInlineAdmin(admin.TabularInline):
    model = ProductionOrderComponent
    extra = 0
    fields = ('bom_item', 'product', 'variant', 'batch', 'planned_qty', 'actual_qty', 'uom', 'reservation')
    readonly_fields = ('actual_qty', 'reservation')
    autocomplete_fields = ('product', 'variant', 'batch')


@admin.register(ProductionOrder)
class ProductionOrderAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'product', 'bill_of_materials', 'planned_qty', 'status', 'completed_at')
    list_filter = ('workspace', 'status')
    search_fields = ('product__title',)
    autocomplete_fields = ('product', 'bill_of_materials', 'finished_serial_unit', 'finished_batch')
    readonly_fields = ('completed_at', 'aggregation_group', 'last_modification', 'date_of_creation')
    inlines = [ProductionOrderComponentInlineAdmin]
    actions = ['action_explode_bom', 'action_release', 'action_start', 'action_cancel']

    def action_explode_bom(self, request, queryset):
        for production_order in queryset:
            try:
                explode(production_order.bill_of_materials)
            except (ValidationError, ExplosionDepthExceeded) as exc:
                self.message_user(request, str(exc), level=messages.ERROR)

    action_explode_bom.short_description = "(Re)compute BillOfMaterialsExplosion snapshot"

    def action_release(self, request, queryset):
        for production_order in queryset:
            try:
                production_order_workflow.release(production_order)
            except ValidationError as exc:
                self.message_user(request, str(exc), level=messages.ERROR)

    action_release.short_description = "Release selected production orders (DRAFT -> RELEASED)"

    def action_start(self, request, queryset):
        for production_order in queryset:
            try:
                production_order_workflow.start(production_order)
            except ValidationError as exc:
                self.message_user(request, str(exc), level=messages.ERROR)

    action_start.short_description = "Start selected production orders (reserve components)"

    def action_cancel(self, request, queryset):
        for production_order in queryset:
            try:
                production_order_workflow.cancel(production_order)
            except ValidationError as exc:
                self.message_user(request, str(exc), level=messages.ERROR)

    action_cancel.short_description = "Cancel selected production orders"
