# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Callable
from zoneinfo import ZoneInfo

from django.utils import timezone

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class TimezoneMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
