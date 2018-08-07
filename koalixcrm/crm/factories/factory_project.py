# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Project
from koalixcrm.crm.factories import GoodProjectStatusFactory
from koalixcrm.djangoUserExtension.tests.factories.factory_project_status import GoodDefaultTemplateSet
from koalixcrm.crm.factories import GoodUserFactory


class GoodProjectFactory(factory.Factory):
    class Meta:
        model = Project

    project_manager = factory.SubFactory(GoodUserFactory)
    project_name = "This is a Test Project"
    description = "This is description of a test Project"
    project_status = factory.SubFactory(GoodProjectStatusFactory)
    default_template_set = factory.SubFactory(GoodDefaultTemplateSet)
    date_of_creation = "2018-05-01"
    last_modification = "2018-05-02"
    last_modified_by = factory.SubFactory(GoodUserFactory)