# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ValidationError
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from koalixcrm.crm.documents.pdf_export import PDFExport
from koalixcrm.global_support_functions import *
from koalixcrm.crm.exceptions import ReportingPeriodDoneDeleteNotPossible
from django.contrib import messages


class Resource(models.Model):
    default_cost
    ressource_type
