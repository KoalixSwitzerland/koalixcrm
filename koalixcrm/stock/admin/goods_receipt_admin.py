# -*- coding: utf-8 -*-
"""GoodsReceiptAdmin for koalixcrm stock (ADR-0017). Admin actions route the
DRAFT/IN_PROGRESS/COMPLETED/CANCELLED workflow through
`services/goods_receipt_workflow.py` so the admin UI stays a first-class
operable surface for UC-0010, not just a record viewer. Editing is blocked
once a receipt is COMPLETED or CANCELLED."""
from __future__ import annotations

from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.choices import GoodsReceiptStatus
from koalixcrm.stock.models.goods_receipt import GoodsReceipt
from koalixcrm.stock.models.goods_receipt_line import GoodsReceiptLine
from koalixcrm.stock.services import goods_receipt_workflow


class GoodsReceiptLineInlineAdmin(admin.TabularInline):
    model = GoodsReceiptLine
    extra = 1
    fields = ('variant', 'expected_qty', 'received_qty', 'uom', 'batch', 'serial_unit',
              'target_location', 'line_status', 'notes')
    readonly_fields = ('line_status',)
    autocomplete_fields = ('variant', 'batch', 'serial_unit', 'target_location')


@admin.register(GoodsReceipt)
class GoodsReceiptAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'supplier_party', 'external_doc_ref', 'received_at', 'status')
    list_filter = ('workspace', 'status')
    search_fields = ('external_doc_ref', 'supplier_party__display_name')
    autocomplete_fields = ('supplier_party',)
    readonly_fields = ('created_at',)
    inlines = [GoodsReceiptLineInlineAdmin]
    actions = ['action_start', 'action_confirm_lines', 'action_complete', 'action_cancel']

    def action_start(self, request, queryset):
        for goods_receipt in queryset:
            try:
                goods_receipt_workflow.start(goods_receipt)
            except ValidationError as exc:
                self.message_user(request, str(exc), level=messages.ERROR)

    action_start.short_description = "Start selected goods receipts (DRAFT -> IN_PROGRESS)"

    def action_confirm_lines(self, request, queryset):
        for goods_receipt in queryset:
            for line in goods_receipt.lines.all():
                try:
                    goods_receipt_workflow.confirm_line(line)
                except ValidationError as exc:
                    self.message_user(request, str(exc), level=messages.ERROR)

    action_confirm_lines.short_description = "Confirm all lines (derive line_status from received_qty)"

    def action_complete(self, request, queryset):
        for goods_receipt in queryset:
            try:
                goods_receipt_workflow.complete(goods_receipt, created_by=request.user)
            except ValidationError as exc:
                self.message_user(request, str(exc), level=messages.ERROR)

    action_complete.short_description = "Complete selected goods receipts (post StockMovements)"

    def action_cancel(self, request, queryset):
        for goods_receipt in queryset:
            try:
                goods_receipt_workflow.cancel(goods_receipt)
            except ValidationError as exc:
                self.message_user(request, str(exc), level=messages.ERROR)

    action_cancel.short_description = "Cancel selected goods receipts"

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.status in (GoodsReceiptStatus.COMPLETED, GoodsReceiptStatus.CANCELLED):
            return False
        return super().has_change_permission(request, obj)
