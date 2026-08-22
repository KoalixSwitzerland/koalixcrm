# -*- coding: utf-8 -*-
"""StockMovementAdmin for koalixcrm stock (ADR-0011). Append-only: no
change/delete permission. The add-form routes through
`services/movement_posting.post_movement` — never a plain `obj.save()` —
so every admin-created movement also updates `OnHandRecord`/`StockBalance`
synchronously, exactly like the REST posting endpoint."""
from __future__ import annotations

import uuid

from django import forms
from django.contrib import admin
from django.core.exceptions import PermissionDenied

from koalixcrm.stock.models.stock_movement import StockMovement
from koalixcrm.stock.services.movement_posting import post_movement


class StockMovementAdminForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ('event_type', 'business_step', 'occurred_at',
                  'source_location', 'destination_location',
                  'product', 'variant', 'batch', 'serial_unit', 'handling_unit',
                  'parent_serial_unit', 'parent_batch', 'aggregation_group',
                  'qty', 'uom', 'reason_code', 'document_type', 'document_id',
                  'owner_type', 'owner_party', 'disposition', 'idempotency_key',
                  'compensates')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idempotency_key'].required = False
        self.fields['idempotency_key'].initial = uuid.uuid4


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    form = StockMovementAdminForm
    list_display = ('id', 'occurred_at', 'business_step', 'variant', 'qty', 'uom',
                     'source_location', 'destination_location', 'disposition', 'owner_type')
    list_filter = ('workspace', 'business_step', 'event_type', 'disposition', 'owner_type')
    search_fields = ('variant__sku', 'idempotency_key', 'serial_unit__serial_number', 'batch__batch_number')
    date_hierarchy = 'occurred_at'
    autocomplete_fields = ('source_location', 'destination_location', 'product', 'variant',
                           'batch', 'serial_unit', 'handling_unit', 'parent_serial_unit',
                           'parent_batch', 'reason_code', 'owner_party', 'compensates')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        active = getattr(request, 'active_workspace', None)
        if active is not None:
            return qs.filter(workspace=active)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        active = getattr(request, 'active_workspace', None)
        if active is not None:
            related_model = db_field.related_model
            if related_model is not None and hasattr(related_model, 'workspace'):
                kwargs['queryset'] = related_model.objects.filter(workspace=active)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        from django.http import HttpResponseRedirect
        from django.urls import reverse

        self.message_user(request, "Stock movement posted.")
        return HttpResponseRedirect(
            reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_changelist')
        )

    def save_model(self, request, obj, form, change):
        if change:
            raise PermissionDenied("StockMovement rows are immutable and append-only.")

        # A superuser used to get a freshly created 'Default Workspace' here.
        # REQ-0028 AC-10: no code path invents a tenant, and the absence of an
        # active workspace is a refusal rather than a substitution.
        active = getattr(request, 'active_workspace', None)
        if active is None:
            raise PermissionDenied('No active workspace.')

        movement = post_movement(
            workspace=active,
            event_type=obj.event_type,
            business_step=obj.business_step,
            occurred_at=obj.occurred_at,
            variant=obj.variant,
            product=obj.product,
            source_location=obj.source_location,
            destination_location=obj.destination_location,
            batch=obj.batch,
            serial_unit=obj.serial_unit,
            handling_unit=obj.handling_unit,
            parent_serial_unit=obj.parent_serial_unit,
            parent_batch=obj.parent_batch,
            aggregation_group=obj.aggregation_group,
            qty=obj.qty,
            uom=obj.uom,
            reason_code=obj.reason_code,
            document_type=obj.document_type,
            document_id=obj.document_id,
            owner_type=obj.owner_type,
            owner_party=obj.owner_party,
            disposition=obj.disposition,
            idempotency_key=obj.idempotency_key or uuid.uuid4(),
            compensates=obj.compensates,
            created_by=request.user,
        )
        obj.pk = movement.pk
        obj.recorded_at = movement.recorded_at
