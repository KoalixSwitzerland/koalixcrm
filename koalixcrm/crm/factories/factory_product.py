# -*- coding: utf-8 -*-

import factory
from koalixcrm.crm.models import Project
from koalixcrm.crm.factories.factory_unit import StandardUnitFactory
from koalixcrm.djangoUserExtension.factories.factory_template_set import StandardTemplateSetFactory
from koalixcrm.crm.factories.factory_user import StaffUserFactory


class StandardProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project
        django_get_or_create = ('project_name',)

    description = models.TextField(verbose_name=_("Description"),
                                   null=True,
                                   blank=True)
    title = "This is a test Product"
    product_number = "123456"
    default_unit = factory.SubFactory(StandardUnitFactory)
    date_of_creation = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    last_modification = make_date_utc(datetime.datetime(2018, 6, 15, 00))
    last_modified_by = factory.SubFactory(StaffUserFactory)
    tax = factory.SubFactory(StandardUnitFactory)
    accounting_product_categorie = models.ForeignKey('accounting.ProductCategorie',
                                                     verbose_name=_("Accounting Product Categorie"),
                                                     null=True,
                                                     blank="True")

