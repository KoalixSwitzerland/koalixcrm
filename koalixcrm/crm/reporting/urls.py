# coding: utf-8

# DJANGO IMPORTS
from django.conf.urls import url

from koalixcrm.crm.views.time_tracking import work_report

urlpatterns = [
    url(r'^time_tracking/$', work_report, name="monthly_report"),
]