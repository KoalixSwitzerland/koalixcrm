# -*- coding: utf-8 -*-

import factory
from koalixcrm.reporting.models.project import Project
from tests.factories.reporting.project_status_factory import StartedProjectStatusFactory
from tests.factories.djangoUserExtension.factory_template_set import StandardTemplateSetFactory
from tests.factories.contacts.user_factory import StaffUserFactory
from tests.factories.core.currency_factory import StandardCurrencyFactory


class StandardProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project
        django_get_or_create = ('project_name',)

    project_manager = factory.SubFactory(StaffUserFactory)
    project_name = "This is a Test Project"
    description = "This is description of a test Project"
    project_status = factory.SubFactory(StartedProjectStatusFactory)
    default_template_set = factory.SubFactory(StandardTemplateSetFactory)
    default_currency = factory.SubFactory(StandardCurrencyFactory)
    date_of_creation = "2018-05-01"
    last_modification = "2018-05-02"
    last_modified_by = factory.SubFactory(StaffUserFactory)
