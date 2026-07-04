# -*- coding: utf-8 -*-
"""
MovementReasonCodeViewSet for koalixcrm stock. Global lookup table
(ADR-0011 Workspace-Scoping-Matrix) — not workspace-scoped.
"""
from __future__ import annotations

from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.stock.models.movement_reason_code import MovementReasonCode
from koalixcrm.stock.serializers.movement_reason_code_serializer import MovementReasonCodeJSONSerializer


class MovementReasonCodeViewSet(BaseModelViewSet):
    serializer_class = MovementReasonCodeJSONSerializer
    queryset = MovementReasonCode.objects.all()
