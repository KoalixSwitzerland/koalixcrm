# -*- coding: utf-8 -*-

import zoneinfo
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'crm/admin/set_timezone.html', {'timezones': sorted(zoneinfo.available_timezones())})
