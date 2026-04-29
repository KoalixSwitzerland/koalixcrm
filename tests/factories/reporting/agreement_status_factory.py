# -*- coding: utf-8 -*-

import factory

from koalixcrm.reporting.models.agreement_status import AgreementStatus


class AgreedAgreementStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgreementStatus
        django_get_or_create = ('title',)

    title = "Done"
    description = "This agreement is agreed"
    is_agreed = True


class PlannedAgreementStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgreementStatus
        django_get_or_create = ('title',)

    title = "Planned"
    description = "This agreement is planned"
    is_agreed = False


class StartedAgreementStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgreementStatus
        django_get_or_create = ('title',)

    title = "Started"
    description = "This agreement is started"
    is_agreed = False
