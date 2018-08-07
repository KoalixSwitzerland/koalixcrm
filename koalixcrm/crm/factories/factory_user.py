# -*- coding: utf-8 -*-

import factory
from django.contrib.auth.models import User


class GoodUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'admin'
    email = 'admin@admin.com'

    password = factory.PostGenerationMethodCall('set_password', 'admin')

    is_superuser = True
    is_staff = True
    is_active = True
