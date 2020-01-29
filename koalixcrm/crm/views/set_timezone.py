# -*- coding: utf-8 -*-

import pytz
from django.shortcuts import redirect, render


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'crm/admin/set_timezone.html', {'timezones': pytz.common_timezones})
