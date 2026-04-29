# -*- coding: utf-8 -*-
"""Serializers for the ``/projects/{id}/report-data/`` endpoint that feeds
the Java pdf-export-service for the project_report XSL.

Shape mirrors the legacy ``Project.serialize_to_xml`` output 1:1 in JSON
form: every aggregate the XSL reads (``Effective_Effort_Overall``,
``Planned_Effort``, …) is a top-level field, and tasks/works are nested
arrays. The Java side reconstructs the Django-serializer XML the XSL
expects from this payload — see ``ProjectReportXmlBuilder`` in
pdf-export-service.

Aggregate field names are snake_cased here; Java maps them back to the
PascalCase XML element names the XSL queries.
"""
from __future__ import annotations

from typing import Any

from rest_framework import serializers

from koalixcrm.reporting.models.project import Project
from koalixcrm.reporting.models.task import Task
from koalixcrm.reporting.models.work import Work


class _ReportWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'task', 'reporting_period', 'human_resource',
                  'date', 'short_description', 'description',
                  'worked_hours')


class _ReportTaskSerializer(serializers.ModelSerializer):
    """Per-task aggregates that feed the project_report XSL columns."""
    works = serializers.SerializerMethodField()
    effective_costs_confirmed_overall = serializers.SerializerMethodField()
    effective_costs_not_confirmed_overall = serializers.SerializerMethodField()
    effective_effort_overall = serializers.SerializerMethodField()
    effective_costs_in_period = serializers.SerializerMethodField()
    effective_effort_in_period = serializers.SerializerMethodField()
    planned_effort = serializers.SerializerMethodField()
    effective_duration = serializers.SerializerMethodField()
    planned_duration = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'project', 'status',
                  'last_status_change',
                  'works',
                  'effective_costs_confirmed_overall',
                  'effective_costs_not_confirmed_overall',
                  'effective_effort_overall',
                  'effective_costs_in_period',
                  'effective_effort_in_period',
                  'planned_effort',
                  'effective_duration',
                  'planned_duration')

    def _period(self) -> Any:
        return self.context.get('reporting_period')

    def get_works(self, obj: Task) -> Any:
        period = self._period()
        if period:
            qs = Work.objects.filter(task=obj.id, reporting_period=period)
        else:
            qs = Work.objects.filter(task=obj.id)
        return _ReportWorkSerializer(qs, many=True).data

    def get_effective_costs_confirmed_overall(self, obj: Task) -> Any:
        return obj.effective_costs_confirmed()

    def get_effective_costs_not_confirmed_overall(self, obj: Task) -> Any:
        return obj.effective_costs_not_confirmed()

    def get_effective_effort_overall(self, obj: Task) -> Any:
        return obj.effective_effort(reporting_period=None)

    def get_effective_costs_in_period(self, obj: Task) -> Any:
        period = self._period()
        return obj.effective_costs(reporting_period=period) if period else None

    def get_effective_effort_in_period(self, obj: Task) -> Any:
        period = self._period()
        return obj.effective_effort(reporting_period=period) if period else None

    def get_planned_effort(self, obj: Task) -> Any:
        # Mirrors the legacy serialize_to_xml which intentionally calls
        # ``planned_costs()`` (not ``planned_effort()``) for this element.
        return obj.planned_costs()

    def get_effective_duration(self, obj: Task) -> Any:
        return obj.effective_duration()

    def get_planned_duration(self, obj: Task) -> Any:
        return obj.planned_duration()


class _ReportingPeriodRefSerializer(serializers.Serializer):
    """The XSL only reads ``title``; we include id/begin/end for context."""
    id = serializers.IntegerField()
    title = serializers.CharField()
    begin = serializers.DateField()
    end = serializers.DateField()


class _UserExtensionRefSerializer(serializers.Serializer):
    """Compact reference for the project manager / report-of user — the
    work_report XSL reads ``user_extension/user`` and ``object[@model='auth.user']/username``.
    """
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()


class ProjectReportSerializer(serializers.ModelSerializer):
    """Full snapshot for a project_report PDF render. Matches the XSL field
    list element-for-element so Java can recreate the legacy XML byte-shape.
    """
    project_name = serializers.CharField()
    description = serializers.CharField()
    reporting_period = serializers.SerializerMethodField()
    user_extension = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()
    effective_costs_confirmed = serializers.SerializerMethodField()
    effective_costs_not_confirmed = serializers.SerializerMethodField()
    effective_effort_overall = serializers.SerializerMethodField()
    effective_costs_in_period = serializers.SerializerMethodField()
    effective_effort_in_period = serializers.SerializerMethodField()
    planned_total_costs = serializers.SerializerMethodField()
    effective_duration = serializers.SerializerMethodField()
    planned_duration = serializers.SerializerMethodField()
    project_cost_overview_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id',
                  'project_name',
                  'description',
                  'project_status',
                  'project_manager',
                  'default_currency',
                  'default_template_set',
                  'reporting_period',
                  'user_extension',
                  'tasks',
                  'effective_costs_confirmed',
                  'effective_costs_not_confirmed',
                  'effective_effort_overall',
                  'effective_costs_in_period',
                  'effective_effort_in_period',
                  'planned_total_costs',
                  'effective_duration',
                  'planned_duration',
                  'project_cost_overview_url')

    # ---- helpers --------------------------------------------------------

    def _period(self) -> Any:
        return self.context.get('reporting_period')

    # ---- fields ---------------------------------------------------------

    def get_reporting_period(self, obj: Project) -> Any:
        period = self._period()
        if not period:
            return None
        return _ReportingPeriodRefSerializer(period).data

    def get_user_extension(self, obj: Project) -> Any:
        from koalixcrm.djangoUserExtension.models.user_extension import UserExtension
        ref_user = obj.project_manager
        if ref_user is None:
            return None
        ue = UserExtension.objects.filter(user=ref_user.id).first()
        if ue is None:
            return None
        return _UserExtensionRefSerializer({
            'id': ue.id,
            'user_id': ref_user.id,
            'username': ref_user.username,
        }).data

    def get_tasks(self, obj: Project) -> Any:
        tasks = Task.objects.filter(project=obj.id)
        return _ReportTaskSerializer(
            tasks, many=True, context={'reporting_period': self._period()}
        ).data

    def get_effective_costs_confirmed(self, obj: Project) -> Any:
        return obj.effective_costs_confirmed()

    def get_effective_costs_not_confirmed(self, obj: Project) -> Any:
        return obj.effective_costs_not_confirmed()

    def get_effective_effort_overall(self, obj: Project) -> Any:
        return obj.effective_effort(reporting_period=None)

    def get_effective_costs_in_period(self, obj: Project) -> Any:
        period = self._period()
        return obj.effective_costs(reporting_period=period) if period else None

    def get_effective_effort_in_period(self, obj: Project) -> Any:
        period = self._period()
        return obj.effective_effort(reporting_period=period) if period else None

    def get_planned_total_costs(self, obj: Project) -> Any:
        return obj.planned_total_costs()

    def get_effective_duration(self, obj: Project) -> Any:
        return obj.effective_duration()

    def get_planned_duration(self, obj: Project) -> Any:
        return obj.planned_duration()

    def get_project_cost_overview_url(self, obj: Project) -> str:
        # Lazy import: matplotlib pulls in heavy deps at import time and is
        # not needed for any other reporting endpoint.
        from koalixcrm.reporting.services.chart_storage import (
            upload_project_cost_overview_svg,
        )
        return upload_project_cost_overview_svg(obj)
