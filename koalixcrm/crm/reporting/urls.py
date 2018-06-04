# coding: utf-8

# DJANGO IMPORTS
from django.conf.urls import url

from koalixcrm.crm.views.monthlyreport import work_report

urlpatterns = [
    url(r'^monthlyreport/$', work_report, name="monthly_report"),
]