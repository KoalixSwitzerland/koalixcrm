# coding: utf-8

# DJANGO IMPORTS
from django.conf.urls import url

from koalixcrm.crm.views.monthlyreport import MonthlyReportView

urlpatterns = [
    url(r'^monthlyreport/$', MonthlyReportView.work_report, name="monthly_report"),
]