# coding: utf-8

# DJANGO IMPORTS
from django.conf.urls import url

from koalixcrm.crm.views.time_tracking import work_report
from koalixcrm.crm.views.user_extension_missing import user_extension_missing

urlpatterns = [
    url(r'^time_tracking/$', work_report, name="monthly_report"),
    url(r'^user_extension_missing/$', user_extension_missing, name="user_extension_missing"),
]