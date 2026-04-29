# -*- coding: utf-8 -*-
"""Serializer for the ``/human-resources/{id}/work-report-data/`` endpoint.

Mirrors the legacy ``HumanResource.serialize_to_xml`` payload: a date
range, the contributing projects, every Work record, plus the bucketed
day/week/month aggregates the work_report XSL pivots over.

The XSL reads:
  - ``range_from`` / ``range_to`` (text + day/week/week_day/month/year attrs)
  - ``object[@model='djangoUserExtension.userextension']/Day_Work_Hours``
  - …``/Day_Project_Work_Hours`` (per project)
  - …``/Week_Work_Hours``, ``Week_Project_Work_Hours``
  - …``/Month_Work_Hours``, ``Month_Project_Work_Hours``
  - ``object[@model='auth.user' and @pk=$report_of_user]/username``
  - ``object[@model='crm.project']/project_name``
  - ``object[@model='crm.work']``
  - ``user_extension/user``
"""
from __future__ import annotations

import datetime
from typing import Any

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from koalixcrm.reporting.models.human_resource import HumanResource
from koalixcrm.reporting.models.work import Work


class _ProjectRefSerializer(serializers.Serializer):
    """Minimal project ref the work_report XSL needs: pk + project_name."""
    id = serializers.IntegerField()
    project_name = serializers.CharField()


class _BucketAggregateSerializer(serializers.Serializer):
    """One row of (day|week|month, optional project) → effort in hours.

    ``effort`` is a string because the legacy XML used the literal token
    ``"-"`` for days outside the requested range (XSL distinguishes 0,
    "-", and a number to drive cell rendering).
    """
    effort = serializers.CharField()
    project_id = serializers.IntegerField(required=False, allow_null=True)
    day = serializers.CharField(required=False)
    week = serializers.CharField(required=False)
    week_day = serializers.CharField(required=False)
    month = serializers.CharField(required=False)
    year = serializers.CharField(required=False)


class _WorkRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'task', 'reporting_period', 'human_resource',
                  'date', 'short_description', 'description',
                  'worked_hours')


class HumanResourceWorkReportSerializer(serializers.Serializer):
    """Read-only: built by ``WorkReportBuilder`` rather than via Meta.fields,
    because the day/week/month buckets aren't model fields.
    """
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    range_from = serializers.DateField()
    range_to = serializers.DateField()
    projects = _ProjectRefSerializer(many=True)
    works = _WorkRowSerializer(many=True)
    day_buckets = _BucketAggregateSerializer(many=True)
    day_project_buckets = _BucketAggregateSerializer(many=True)
    week_buckets = _BucketAggregateSerializer(many=True)
    week_project_buckets = _BucketAggregateSerializer(many=True)
    month_buckets = _BucketAggregateSerializer(many=True)
    month_project_buckets = _BucketAggregateSerializer(many=True)


def _isokeys(d: datetime.date) -> dict[str, str]:
    iso = d.isocalendar()
    return {
        "day": str(d.day),
        "week": str(iso[1]),
        "week_day": str(d.isoweekday()),
        "month": str(d.month),
        "year": str(d.year),
    }


class WorkReportBuilder:
    """Produces the dict structure that ``HumanResourceWorkReportSerializer``
    consumes. Logic lifted verbatim from
    ``HumanResource.serialize_to_xml`` so the bucket cell semantics
    (``"-"`` for days outside range, "0" before any work is added) match
    byte-for-byte with the legacy output.
    """

    def __init__(self, human_resource: HumanResource,
                 date_from: datetime.date, date_to: datetime.date) -> None:
        self.hr = human_resource
        self.date_from = date_from
        self.date_to = date_to

    def build(self) -> dict[str, Any]:
        hr = self.hr
        date_from, date_to = self.date_from, self.date_to
        date_first_of_month = date_from.replace(day=1)
        date_first_of_next_month = date_first_of_month + relativedelta(months=+1)
        date_end_of_month = date_first_of_next_month - datetime.timedelta(days=1)

        projects = hr.resource_contribution_project(date_from, date_to)
        # day_key -> {effort, attrs..., project_efforts: {project_id: {effort, project}}}
        days, weeks, months = {}, {}, {}

        date = date_first_of_month
        while date < date_from:
            project_efforts = {p.id: {'effort': "-", 'project_id': p.id} for p in projects}
            days[date] = {'effort': "-", **_isokeys(date), 'project_efforts': project_efforts}
            date += datetime.timedelta(days=1)

        while date <= date_to:
            day_pe = {p.id: {'effort': 0, 'project_id': p.id} for p in projects}
            week_pe = {p.id: {'effort': 0, 'project_id': p.id} for p in projects}
            month_pe = {p.id: {'effort': 0, 'project_id': p.id} for p in projects}
            days[date] = {'effort': 0, **_isokeys(date), 'project_efforts': day_pe}
            month_key = f"{date.month}/{date.year}"
            week_key = f"{date.isocalendar()[1]}/{date.year}"
            weeks.setdefault(week_key, {
                'effort': 0,
                'week': str(date.isocalendar()[1]),
                'year': str(date.year),
                'project_efforts': week_pe,
            })
            months.setdefault(month_key, {
                'effort': 0,
                'month': str(date.month),
                'year': str(date.year),
                'project_efforts': month_pe,
            })
            date += datetime.timedelta(days=1)

        while date < date_end_of_month:
            project_efforts = {p.id: {'effort': "-", 'project_id': p.id} for p in projects}
            days[date] = {'effort': "-", **_isokeys(date), 'project_efforts': project_efforts}
            date += datetime.timedelta(days=1)

        works = list(Work.objects.filter(human_resource=hr, date__range=(date_from, date_to)))
        for w in works:
            hours = w.effort_hours()
            project_id = w.task.project_id
            if isinstance(days[w.date]['effort'], str):
                days[w.date]['effort'] = 0
            days[w.date]['effort'] += hours
            day_pe_entry = days[w.date]['project_efforts'].setdefault(
                project_id, {'effort': 0, 'project_id': project_id})
            if isinstance(day_pe_entry['effort'], str):
                day_pe_entry['effort'] = 0
            day_pe_entry['effort'] += hours

            month_key = f"{w.date.month}/{w.date.year}"
            week_key = f"{w.date.isocalendar()[1]}/{w.date.year}"
            weeks[week_key]['effort'] += hours
            week_pe_entry = weeks[week_key]['project_efforts'].setdefault(
                project_id, {'effort': 0, 'project_id': project_id})
            week_pe_entry['effort'] += hours
            months[month_key]['effort'] += hours
            month_pe_entry = months[month_key]['project_efforts'].setdefault(
                project_id, {'effort': 0, 'project_id': project_id})
            month_pe_entry['effort'] += hours

        def _flatten_day_pe() -> list[dict[str, Any]]:
            rows = []
            for day_key in sorted(days.keys()):
                meta = days[day_key]
                for pid, pe in meta['project_efforts'].items():
                    rows.append({
                        'effort': str(pe['effort']),
                        'project_id': pid,
                        'day': meta['day'], 'week': meta['week'],
                        'week_day': meta['week_day'],
                        'month': meta['month'], 'year': meta['year'],
                    })
            return rows

        def _flatten_days() -> list[dict[str, Any]]:
            return [{
                'effort': str(meta['effort']),
                'day': meta['day'], 'week': meta['week'],
                'week_day': meta['week_day'],
                'month': meta['month'], 'year': meta['year'],
            } for _, meta in sorted(days.items())]

        def _flatten_week_or_month_pe(buckets: dict[str, Any], kind: str) -> list[dict[str, Any]]:
            rows = []
            for _, meta in buckets.items():
                for pid, pe in meta['project_efforts'].items():
                    row = {
                        'effort': str(pe['effort']),
                        'project_id': pid,
                        'year': meta['year'],
                    }
                    if kind == 'week':
                        row['week'] = meta['week']
                    else:
                        row['month'] = meta['month']
                    rows.append(row)
            return rows

        def _flatten_week_or_month(buckets: dict[str, Any], kind: str) -> list[dict[str, Any]]:
            rows = []
            for _, meta in buckets.items():
                row = {'effort': str(meta['effort']), 'year': meta['year']}
                if kind == 'week':
                    row['week'] = meta['week']
                else:
                    row['month'] = meta['month']
                rows.append(row)
            return rows

        return {
            'id': hr.id,
            'user_id': hr.user.user_id,
            'username': hr.user.user.username,
            'range_from': date_from,
            'range_to': date_to,
            'projects': [{'id': p.id, 'project_name': p.project_name} for p in projects],
            'works': _WorkRowSerializer(works, many=True).data,
            'day_buckets': _flatten_days(),
            'day_project_buckets': _flatten_day_pe(),
            'week_buckets': _flatten_week_or_month(weeks, 'week'),
            'week_project_buckets': _flatten_week_or_month_pe(weeks, 'week'),
            'month_buckets': _flatten_week_or_month(months, 'month'),
            'month_project_buckets': _flatten_week_or_month_pe(months, 'month'),
        }
