# -*- coding: utf-8 -*-
"""
WorkspaceScopedModelAdmin — mixin for ModelAdmin classes whose model inherits
WorkspaceScopedModel.

CR-9 §9.5.
"""

from django.core.exceptions import PermissionDenied


class WorkspaceScopedModelAdmin:
    """Mixin to scope ModelAdmin to the request's active workspace."""

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

    def save_model(self, request, obj, form, change):
        active = getattr(request, 'active_workspace', None)

        # Assign workspace if not yet set.
        if obj.workspace_id is None:
            if active is None:
                raise PermissionDenied('No active workspace.')
            obj.workspace_id = active.id

        # Validate the object belongs to the active workspace.
        if active is not None and not request.user.is_superuser:
            if obj.workspace_id != active.id:
                raise PermissionDenied(
                    'Object workspace does not match the active workspace.'
                )

            # Validate all FK fields pointing to workspace-scoped rows.
            for field in obj._meta.get_fields():
                if not hasattr(field, 'related_model') or field.related_model is None:
                    continue
                if not hasattr(field, 'column'):
                    continue
                related_model = field.related_model
                if not hasattr(related_model, 'workspace'):
                    continue
                fk_value = getattr(obj, field.attname, None)
                if fk_value is None:
                    continue
                if not related_model.objects.filter(
                    pk=fk_value, workspace_id=active.id
                ).exists():
                    raise PermissionDenied(
                        f'Related {related_model.__name__} (pk={fk_value}) '
                        f'does not belong to the active workspace.'
                    )

        super().save_model(request, obj, form, change)
