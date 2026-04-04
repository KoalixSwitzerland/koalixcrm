# -*- coding: utf-8 -*-
"""
Django User Extension API entry point.

Exposes User Extension REST viewsets for URL routing.
"""
from koalixcrm.djangoUserExtension.serializers.user_rest import UserAsJSON

__all__ = [
    'UserAsJSON',
]
