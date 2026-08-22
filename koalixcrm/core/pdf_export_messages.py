# -*- coding: utf-8 -*-
"""
Shared success message for the asynchronous PDF-export admin actions.

The actions only enqueue a :class:`PDFExportProcess`; the resulting PDF shows
up later. The message therefore has to point the user at the process list —
as an actual link, since the Grappelli dashboard is a curated set of modules
and users cannot be expected to guess the admin URL.
"""
from __future__ import annotations

from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _


def pdf_export_queued_message(count: int, label: str | None = None):
    """
    Build the "N job(s) queued" message with a link to the process list.

    ``label`` names the kind of document (e.g. "Balance Sheet"); when omitted
    the generic "PDF export" wording is used. Returns a ``SafeString``, which
    the messages framework renders unescaped.
    """
    if label:
        text = _("%(count)d %(label)s job(s) queued.") % {
            "count": count,
            "label": label,
        }
    else:
        text = _("%(count)d PDF export job(s) queued.") % {"count": count}

    return format_html(
        '{} <a href="{}">{}</a>',
        text,
        reverse("admin:core_pdfexportprocess_changelist"),
        _("Check PDF Export Processes for status."),
    )
