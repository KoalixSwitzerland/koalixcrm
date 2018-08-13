# -*- coding: utf-8 -*-

import factory
from django.contrib.auth.models import User


class StaffUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'staff_user'
    email = 'staff_user@staff_user.com'

    password = factory.PostGenerationMethodCall('set_password', 'staff_user')

    is_superuser = False
    is_staff = True
    is_active = True


class AdminUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'admin'
    email = 'admin@admin.com'

    password = factory.PostGenerationMethodCall('set_password', 'admin')

    is_superuser = True
    is_staff = True
    is_active = True


class StandardUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'standard'
    email = 'standard@standard.com'

    password = factory.PostGenerationMethodCall('set_password', 'standard')

    is_superuser = False
    is_staff = False
    is_active = True
