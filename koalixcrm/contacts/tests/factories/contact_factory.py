# -*- coding: utf-8 -*-
"""Factory for the new Party pattern (post-v2.0.0 / issue #395 G3).

`StandardContactFactory` still exists by name for downstream factory
inheritance, but it now produces a `contacts.Organization` (Party
subclass) instead of the legacy `contacts.Contact`. Tests that expected
legacy-Contact-only attributes need targeted updates.
"""
import factory

from koalixcrm.contacts.models.organization import Organization
from koalixcrm.contacts.tests.factories.user_factory import StaffUserFactory
from koalixcrm.core.tests.factories.workspace_factory import DefaultWorkspaceFactory


class StandardContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    workspace = factory.SubFactory(DefaultWorkspaceFactory)
    display_name = factory.Sequence(lambda n: f"Fixture Org {n}")
    legal_name = factory.LazyAttribute(lambda o: o.display_name)
    last_modified_by = factory.SubFactory(StaffUserFactory)
