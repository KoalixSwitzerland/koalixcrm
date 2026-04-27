"""ProjectViewSet for koalixcrm reporting."""
from rest_framework import status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response

from koalixcrm.shared.base_model_view_set import BaseModelViewSet

from ..models.project import Project
from ..models.reporting_period import ReportingPeriod
from ..serializers.project_report_serializer import ProjectReportSerializer
from ..serializers.project_serializer import ProjectJSONSerializer


class ProjectViewSet(BaseModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectJSONSerializer

    @action(detail=True, methods=['get'], url_path='report-data')
    def report_data(self, request, pk=None, **kwargs):
        """Self-contained snapshot for the project_report XSL: project meta +
        nested tasks + per-task aggregates + presigned URL of the cost
        overview chart. Pass ``?reporting_period=<id>`` for a period-scoped
        report; omit for an overall report.
        """
        project = self.get_object()
        period = None
        period_id = request.query_params.get('reporting_period')
        if period_id:
            try:
                period = ReportingPeriod.objects.get(pk=int(period_id), project=project)
            except (ReportingPeriod.DoesNotExist, ValueError):
                return Response(
                    {'detail': f"reporting_period {period_id!r} not found for project {project.id}"},
                    status=http_status.HTTP_404_NOT_FOUND,
                )
        serializer = ProjectReportSerializer(
            project, context={'reporting_period': period, 'request': request}
        )
        return Response(serializer.data)
