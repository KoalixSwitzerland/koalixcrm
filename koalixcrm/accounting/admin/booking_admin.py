# -*- coding: utf-8 -*-
from django.contrib import admin
from koalixcrm.accounting.accounting.booking import Booking, OptionBooking

admin.site.register(Booking, OptionBooking)
