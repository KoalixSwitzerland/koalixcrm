# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import EstimationStatus


class ObsoleteEstimationStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EstimationStatus
        django_get_or_create = ('title',)

    title = "Done"
    description = "This estimation is obsolete"
    is_obsolete = True


class PlannedEstimationStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EstimationStatus
        django_get_or_create = ('title',)

    title = "Planned"
    description = "This estimation is planned"
    is_obsolete = False


class StartedEstimationStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EstimationStatus
        django_get_or_create = ('title',)

    title = "Started"
    description = "This estimation is started"
    is_obsolete = False
