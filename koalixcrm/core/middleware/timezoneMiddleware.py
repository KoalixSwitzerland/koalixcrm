# -*- coding: utf-8 -*-
from zoneinfo import ZoneInfo

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
