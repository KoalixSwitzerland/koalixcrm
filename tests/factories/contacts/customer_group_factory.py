# -*- coding: utf-8 -*-
"""Customer-group factory (post-v2.0.0 / issue #395 G3).

Creates a PartyGroup with `role_type_scope='customer'` — the v2.0.0
equivalent of the legacy CustomerGroup model. The class name is kept
for downstream test compatibility; the underlying model is PartyGroup.
"""
import factory

from koalixcrm.contacts.models.party_group import PartyGroup
from tests.factories.core.workspace_factory import DefaultWorkspaceFactory


class StandardCustomerGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PartyGroup
        django_get_or_create = ('name',)

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    name = factory.Sequence(lambda n: f"Fixture Party Group {n}")
    role_type_scope = 'customer'


class AdvancedCustomerGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PartyGroup

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    name = factory.Sequence(lambda n: f"Fixture Party Group adv {n}")
    role_type_scope = 'customer'
