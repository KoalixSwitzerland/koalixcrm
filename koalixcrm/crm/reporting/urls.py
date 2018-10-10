# coding: utf-8

# DJANGO IMPORTS
from django.conf.urls import url

from koalixcrm.crm.views.time_tracking import work_report
from koalixcrm.crm.views.user_extension_missing import user_extension_missing
from koalixcrm.crm.views.reporting_period_missing import reporting_period_missing
from koalixcrm.crm.views.user_is_not_human_resource import user_is_not_human_resource

urlpatterns = [
    url(r'^time_tracking/$', work_report, name="monthly_report"),
    url(r'^user_extension_missing/$', user_extension_missing, name="user_extension_missing"),
    url(r'^reporting_period_missing/$', reporting_period_missing, name="reporting_period_missing"),
    url(r'^user_is_not_human_resource/$', user_is_not_human_resource, name="user_is_not_human_resource"),
]