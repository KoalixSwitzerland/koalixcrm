# coding: utf-8

# DJANGO IMPORTS
from django.urls import path

from koalixcrm.crm.views.time_tracking import work_report
from koalixcrm.crm.views.user_extension_missing import user_extension_missing
from koalixcrm.crm.views.reporting_period_missing import reporting_period_missing
from koalixcrm.crm.views.user_is_not_human_resource import user_is_not_human_resource
from koalixcrm.crm.views.set_timezone import set_timezone

urlpatterns = [
    path('time_tracking/', work_report, name="monthly_report"),
    path('user_extension_missing/', user_extension_missing, name="user_extension_missing"),
    path('reporting_period_missing/', reporting_period_missing, name="reporting_period_missing"),
    path('user_is_not_human_resource/', user_is_not_human_resource, name="user_is_not_human_resource"),
    path('set_timezone/', set_timezone, name="set_timezone"),
]