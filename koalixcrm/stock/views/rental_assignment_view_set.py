# -*- coding: utf-8 -*-
"""
RentalAssignmentViewSet for koalixcrm stock (ADR-0013).
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.shared.workspace_scoped_view_set import WorkspaceScopedViewSetMixin
from koalixcrm.stock.models.rental_assignment import RentalAssignment
from koalixcrm.stock.serializers.rental_assignment_serializer import RentalAssignmentJSONSerializer


class RentalAssignmentViewSet(WorkspaceScopedViewSetMixin, BaseModelViewSet):
    serializer_class = RentalAssignmentJSONSerializer
    queryset = RentalAssignment.objects.all()
