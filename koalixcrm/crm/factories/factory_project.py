# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Project
from koalixcrm.crm.factories.factory_project_status import StandardProjectStatusFactory
from koalixcrm.djangoUserExtension.factories import StandardDefaultTemplateSet
from koalixcrm.crm.factories.factory_user import StaffUserFactory


class StandardProjectFactory(factory.Factory):
    class Meta:
        model = Project

    project_manager = factory.SubFactory(StaffUserFactory)
    project_name = "This is a Test Project"
    description = "This is description of a test Project"
    project_status = factory.SubFactory(StandardProjectStatusFactory)
    default_template_set = factory.SubFactory(StandardDefaultTemplateSet)
    date_of_creation = "2018-05-01"
    last_modification = "2018-05-02"
    last_modified_by = factory.SubFactory(StaffUserFactory)
