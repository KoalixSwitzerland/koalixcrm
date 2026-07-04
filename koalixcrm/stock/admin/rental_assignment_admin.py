# -*- coding: utf-8 -*-
"""RentalAssignmentAdmin for koalixcrm stock (ADR-0013)."""
from __future__ import annotations

from django.contrib import admin

from koalixcrm.core.admin.workspace_scoped_admin import WorkspaceScopedModelAdmin
from koalixcrm.stock.models.rental_assignment import RentalAssignment


@admin.register(RentalAssignment)
class RentalAssignmentAdmin(WorkspaceScopedModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'serial_unit', 'party', 'rental_start', 'return_due_date',
                     'returned_at', 'status', 'condition_at_return')
    list_filter = ('workspace', 'status', 'condition_at_return')
    search_fields = ('serial_unit__serial_number', 'party__display_name')
    autocomplete_fields = ('serial_unit', 'on_hand_record', 'reservation', 'party')
    readonly_fields = ('date_of_creation', 'last_modification')
