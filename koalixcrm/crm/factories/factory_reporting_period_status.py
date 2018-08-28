# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import ReportingPeriodStatus


class InPreparationReportingPeriodStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportingPeriodStatus
        django_get_or_create = ('title',)

    title = "In Preparation"
    description = "In Preparation, reporting not yet enabled"
    is_done = False


class ReportingReportingPeriodStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportingPeriodStatus
        django_get_or_create = ('title',)

    title = "Reporting"
    description = "Reporting is enabled"
    is_done = False


class DoneReportingPeriodStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportingPeriodStatus
        django_get_or_create = ('title',)

    title = "Done"
    description = "This reporting period is done"
    is_done = True
