# -*- coding: utf-8 -*-
"""Abstract base for S3-stored media, ported from the Workflow Support Webapp.

Mirrors ``qq_workflow_support.models.s3_media`` (WFS ADR-7 / QUAQ2-110). The
central rule it carries over: **the database stores a relative S3 object key,
never an absolute URI**.

That rule is not cosmetic. An absolute URL bakes the endpoint host into the
row, so a value written by a container (``http://minio:9000/bucket/key``) is
meaningless to a browser, to a different environment, or after an endpoint
change. Storing the key instead lets every reader build the URL it needs —
which is exactly what presigned downloads require.

Adapted from WFS in one respect: WFS models ``media_type`` as an FK to a
``MediaType`` table. koalixCRM keeps its existing free-form MIME ``CharField``
rather than dragging that table in.
"""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = [
    ("pending", _("Pending")),
    ("uploaded", _("Uploaded")),
    ("processing", _("Processing")),
    ("completed", _("Completed")),
    ("failed", _("Failed")),
]

_ABSOLUTE_PREFIXES = ("s3://", "http://", "https://")


def validate_s3_url_is_relative(value: str) -> None:
    """Reject any ``s3_url`` that looks like an absolute URI.

    Absolute forms such as ``s3://bucket/key``,
    ``https://bucket.s3.amazonaws.com/key`` or ``http://minio:9000/bucket/key``
    must never reach the DB; whoever uploads is responsible for stripping the
    scheme and bucket before writing.

    Intentionally permissive for blank values so a ``pending`` row can exist
    before any upload has happened.
    """
    if not value:
        return
    if value.lower().startswith(_ABSOLUTE_PREFIXES):
        raise ValidationError(
            _("s3_url must be a relative S3 object key, not an absolute URI. Got: %(value)r"),
            params={"value": value},
        )


class S3Media(models.Model):
    """Abstract base for all S3-stored media files.

    Concrete subclasses add the parent FK, workspace scoping and audit fields.
    """

    s3_url = models.CharField(
        verbose_name=_("S3 Key"),
        max_length=500,
        blank=True,
        default="",
        validators=[validate_s3_url_is_relative],
        help_text=_("Relative object key inside the bucket — never an absolute URL."),
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    media_type = models.CharField(
        verbose_name=_("Media Type"),
        max_length=50,
        default="application/pdf",
        help_text=_("MIME type of the stored file"),
    )

    class Meta:
        abstract = True

    @property
    def filename(self) -> str:
        """Trailing path segment of the key — enough for at-a-glance display."""
        return self.s3_url.rsplit("/", 1)[-1] if self.s3_url else ""

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.pk}"
