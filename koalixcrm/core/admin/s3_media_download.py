# -*- coding: utf-8 -*-
"""Shared presigned-download-link helper for S3Media admins.

Lives in ``core`` beside :mod:`koalixcrm.core.models.s3_media`, so every app
with S3-backed media can use it without ``core`` depending on ``contracts``.

Ported from the Workflow Support Webapp (``contracts/admin/_media_download.py``).
Both the ModelAdmin and the inline on the parent document expose the same
clickable column, so the markup-producing helper lives here and each admin just
imports ``download_link_html`` or mixes in ``S3MediaDownloadMixin``.

Presigned URLs are generated for ``uploaded`` / ``completed`` rows only —
anything else has no real object in S3 yet.
"""
from __future__ import annotations

import logging
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import SafeString
from django.utils.translation import gettext as _

from koalixcrm_utils.aws_clients import get_s3_presign_client

logger = logging.getLogger(__name__)

DEFAULT_PRESIGN_TTL_SECONDS = 300

READY_STATUSES = ("uploaded", "completed")

_ABSOLUTE_PREFIXES = ("s3://", "http://", "https://")


def presigned_url_for_key(s3_key: str) -> str:
    """Return a short-lived presigned GET URL for ``s3_key``, or ``''``.

    Signed against the *public* endpoint so the host in the URL is one the
    browser can actually reach. Any boto/config error is logged and swallowed —
    a storage problem must never take the admin page down with it.
    """
    if not s3_key:
        return ""
    try:
        bucket = settings.S3_MEDIA_BUCKET
        ttl = getattr(settings, "PRESIGNED_DOWNLOAD_URL_EXPIRY", DEFAULT_PRESIGN_TTL_SECONDS)
        return get_s3_presign_client().generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": s3_key},
            ExpiresIn=ttl,
        )
    except Exception:
        logger.exception("Failed to generate presigned URL for key %r", s3_key)
        return ""


def s3_key_from_url(value: str, bucket: str = "") -> str:
    """Best-effort object key from a value that may be an absolute URI.

    New rows store a relative key already and pass straight through. Legacy
    rows (and ``PDFExportProcess.result_url``, which the worker still writes as
    an absolute URL) carry ``s3://bucket/key`` or
    ``http://host[:port]/bucket/key``, so the scheme, host and leading bucket
    segment are stripped.
    """
    if not value:
        return ""
    if not value.lower().startswith(_ABSOLUTE_PREFIXES):
        return value.lstrip("/")

    if value.lower().startswith("s3://"):
        remainder = value.split("://", 1)[1]
        # s3://bucket/key -> key
        return remainder.split("/", 1)[1] if "/" in remainder else ""

    path = urlparse(value).path.lstrip("/")
    if bucket and (path == bucket or path.startswith(f"{bucket}/")):
        path = path[len(bucket):].lstrip("/")
    return path


def download_link_html(obj) -> SafeString:
    """Render the filename as an ``<a>`` pointing at a presigned download URL.

    Falls back to ``-`` when there is no key, the row is not ready, or
    presigning failed.
    """
    s3_key = getattr(obj, "s3_url", "") or ""
    status = getattr(obj, "status", None)
    if not s3_key or status not in READY_STATUSES:
        return format_html("-")

    url = presigned_url_for_key(s3_key)
    if not url:
        return format_html("-")

    filename = s3_key.rsplit("/", 1)[-1] or s3_key
    return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', url, filename)


class S3MediaDownloadMixin:
    """Provides the ``download_link`` admin column.

    Mixed into both the ModelAdmin and the TabularInline so they expose an
    identical clickable column without duplicating the helper.
    """

    @admin.display(description=_("File"))
    def download_link(self, obj) -> SafeString:
        return download_link_html(obj)
