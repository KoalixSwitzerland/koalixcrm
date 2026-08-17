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

from koalixcrm.shared.permissions import ReadModelPermissions
from koalixcrm.stock.models.serial_unit import SerialUnit
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
    # A POST that only reads, so the model right required is `view`, not `add`
    # (REQ-0028 AC-6). The queryset names the model the permission guards;
    # `SerialUnit` is the primary entity of the identifier space this resolves
    # over. The view does not iterate it.
    queryset = SerialUnit.objects.none()
    permission_classes = [IsAuthenticated, ReadModelPermissions]

    def _resolve_workspace(self, request, workspace_id=None):
        """The workspace in force, or None.

        `active_workspace` is already the URL workspace — WorkspaceContext-
        Middleware gives the `workspace_id` segment precedence over the
        session. The kwarg is re-read only for stacks without that middleware.
        There is no `Default Workspace` fallback: it used to be created here on
        a superuser request, which is a write on a read path and a tenant the
        operator never asked for (REQ-0028 AC-10).
        """
        from koalixcrm.core.models.workspace import Workspace

        active = getattr(request, 'active_workspace', None)
        if active is not None:
            return active
        if workspace_id is not None:
            try:
                return Workspace.objects.filter(pk=workspace_id, is_active=True).first()
            except (TypeError, ValueError):
                return None
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
