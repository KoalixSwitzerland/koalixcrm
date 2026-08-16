# -*- coding: utf-8 -*-
"""ADR-0016: `POST /api/v1/scan/resolve` (mounted as
`.../scan/resolve/` under the stock app's workspace-scoped URL prefix,
consistent with the app's router-based path shape). Delegates to
`services/scan_resolve.py`."""
from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from koalixcrm.stock.serializers.scan_resolve_serializer import (
    DetailSerializer,
    ScanMatchSerializer,
    ScanResolveConflictSerializer,
    ScanResolveRequestSerializer,
)
from koalixcrm.stock.services import scan_resolve


@extend_schema(
    tags=['scan'],
    summary="Resolve a scanned code to a stock entity",
    description=(
        "Two-stage resolution per ADR-0016: GS1 element-string parsing first, "
        "then exact free-text match. GS1 always wins; free text is only "
        "attempted when no GS1 AI prefix was recognized at all."
    ),
    request=ScanResolveRequestSerializer,
    responses={
        200: ScanMatchSerializer,
        400: DetailSerializer,
        404: DetailSerializer,
        409: ScanResolveConflictSerializer,
    },
)
class ScanResolveView(APIView):
    permission_classes = [IsAuthenticated]

    def _resolve_workspace(self, request, workspace_id=None):
        from koalixcrm.core.models.workspace import Workspace

        active = getattr(request, 'active_workspace', None)
        if active is not None:
            return active
        if workspace_id is not None:
            ws = Workspace.objects.filter(pk=workspace_id, is_active=True).first()
            if ws is not None:
                return ws
        if getattr(request.user, 'is_superuser', False):
            ws, _ = Workspace.objects.get_or_create(
                name='Default Workspace', defaults={'is_active': True},
            )
            return ws
        return None

    def post(self, request, workspace_id=None):
        code = request.data.get('code')
        if not code:
            return Response({"detail": "'code' is required."}, status=status.HTTP_400_BAD_REQUEST)

        workspace = self._resolve_workspace(request, workspace_id)
        if workspace is None:
            return Response({"detail": "No active workspace."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            match = scan_resolve.resolve(code, workspace=workspace)
        except scan_resolve.ScanNotFound:
            return Response({"detail": "No identifier match found."}, status=status.HTTP_404_NOT_FOUND)
        except scan_resolve.ScanMultipleMatches as exc:
            return Response({"detail": "Multiple candidates matched.", "candidates": exc.candidates},
                            status=status.HTTP_409_CONFLICT)

        return Response(match.as_dict())
