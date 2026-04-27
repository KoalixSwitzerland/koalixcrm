# -*- coding: utf-8 -*-
from django.contrib import admin

from koalixcrm.accounting.models.booking import Booking, OptionBooking

admin.site.register(Booking, OptionBooking)
