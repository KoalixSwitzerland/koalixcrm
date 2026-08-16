# -*- coding: utf-8 -*-
"""StockReservationAdmin for koalixcrm stock (ADR-0010). Fully editable;
admin actions route the offer-lifecycle-equivalent transitions through
services/reservation_lifecycle.py so first-SENT-wins is enforced from the
admin UI too."""
from __future__ import annotations

from django.contrib import admin, messages

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.stock_reservation import StockReservation
from koalixcrm.stock.services import reservation_lifecycle


@admin.register(StockReservation)
class StockReservationAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'kind', 'variant', 'serial_unit', 'location', 'qty_reserved',
                     'status', 'reservation_status', 'rental_start', 'rental_end')
    list_filter = ('workspace', 'kind', 'status', 'reservation_status')
    search_fields = ('variant__sku', 'serial_unit__serial_number')
    autocomplete_fields = ('variant', 'location', 'batch', 'serial_unit')
    readonly_fields = ('sent_at', 'date_of_creation', 'last_modification')
    actions = ['action_mark_sent', 'action_confirm', 'action_cancel', 'action_fulfill']

    def action_mark_sent(self, request, queryset):
        for reservation in queryset:
            try:
                reservation_lifecycle.mark_sent(reservation)
            except reservation_lifecycle.ReservationConflict as exc:
                self.message_user(request, str(exc), level=messages.ERROR)

    def action_confirm(self, request, queryset):
        for reservation in queryset:
            reservation_lifecycle.confirm(reservation)

    def action_cancel(self, request, queryset):
        for reservation in queryset:
            reservation_lifecycle.cancel(reservation)

    def action_fulfill(self, request, queryset):
        for reservation in queryset:
            reservation_lifecycle.fulfill(reservation)
