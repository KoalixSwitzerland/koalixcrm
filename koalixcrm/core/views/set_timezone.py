# -*- coding: utf-8 -*-
from __future__ import annotations

import zoneinfo
from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required
def set_timezone(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'crm/admin/set_timezone.html', {'timezones': sorted(zoneinfo.available_timezones())})
