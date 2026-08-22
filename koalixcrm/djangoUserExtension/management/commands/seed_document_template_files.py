# -*- coding: utf-8 -*-
"""Upload the files that existing `DocumentTemplate` rows already point at.

The v2.0.0 `DocumentTemplate` file fields are backed by `TemplateFileStorage`
(S3/MinIO, `templates/` prefix). A database carried over from the filesystem-era
installation still holds names like `xsl/invoice.xsl`, but the bucket that
`minio-setup` creates is empty — nothing ever uploaded the referenced objects.
The PDF worker then dies on `404 … /koalixcrm-pdf-exports/templates/xsl/invoice.xsl`.

This command closes that gap: for every `DocumentTemplate` file field it checks
whether the object exists in storage and, when it does not, uploads the matching
file from a source directory (by default the legacy media tree that ships in the
repo).

Names are matched by basename, falling back to the name with Django's 7-character
collision suffix stripped — the DB refers to `fop_config/fontconfig_tOYVu30.xml`
while the repo ships the original `fontconfig.xml`.

Idempotent: objects that already exist are left untouched, so re-running after
adding a template converges instead of duplicating. Never edits the database —
the stored names are treated as the source of truth and only storage is filled in.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from koalixcrm.djangoUserExtension.models.document_template import DocumentTemplate

FILE_FIELDS = ("xsl_file", "fop_config_file", "logo")

# The v1 template files are legacy production assets and live OUTSIDE the repo
# working tree, because that tree also carried customer data. Point
# KOALIXCRM_LEGACY_TEMPLATE_DIR at wherever they are kept; the in-repo relative
# path remains only as a fallback for a checkout that still has the old tree.
LEGACY_TEMPLATE_DIR_ENV = "KOALIXCRM_LEGACY_TEMPLATE_DIR"
FALLBACK_SOURCE_DIR = "auftraegekoalixnet/media/uploads/templatefiles"
DEFAULT_SOURCE_DIR = os.environ.get(LEGACY_TEMPLATE_DIR_ENV) or FALLBACK_SOURCE_DIR

# Django appends a 7-character random suffix on name collisions:
# `fontconfig.xml` -> `fontconfig_tOYVu30.xml`.
_SUFFIX_RE = re.compile(r"_[A-Za-z0-9]{7}$")


def candidate_basenames(stored_name: str) -> list[str]:
    """Basenames to look for, most specific first."""
    basename = Path(stored_name).name
    names = [basename]
    stem, suffix = Path(basename).stem, Path(basename).suffix
    stripped = _SUFFIX_RE.sub("", stem)
    if stripped != stem:
        names.append(f"{stripped}{suffix}")
    return names


class Command(BaseCommand):
    help = (
        "Upload the files referenced by existing DocumentTemplate rows into the "
        "configured template storage. Idempotent; does not modify the database."
    )

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "--source-dir",
            default=DEFAULT_SOURCE_DIR,
            help=f"Directory holding the template assets (default: {DEFAULT_SOURCE_DIR})",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would be uploaded without writing to storage.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        source_dir = Path(options["source_dir"])
        if not source_dir.is_dir():
            raise CommandError(f"Source directory does not exist: {source_dir}")

        dry_run = options["dry_run"]
        uploaded = skipped = missing = 0

        for template in DocumentTemplate.objects.all().order_by("pk"):
            for field_name in FILE_FIELDS:
                field = getattr(template, field_name)
                if not field:
                    continue

                stored_name = field.name
                if field.storage.exists(stored_name):
                    skipped += 1
                    continue

                source = self._locate(source_dir, stored_name)
                if source is None:
                    missing += 1
                    self.stderr.write(
                        self.style.WARNING(
                            f"[{template.pk}] {field_name}: no source file for "
                            f"'{stored_name}' in {source_dir}"
                        )
                    )
                    continue

                if dry_run:
                    self.stdout.write(f"[{template.pk}] would upload {source} -> {stored_name}")
                    uploaded += 1
                    continue

                with source.open("rb") as handle:
                    saved_name = field.storage.save(stored_name, File(handle))

                if saved_name != stored_name:
                    # file_overwrite=False makes storage rename on collision; a
                    # different name means the row would still point at nothing.
                    self.stderr.write(
                        self.style.WARNING(
                            f"[{template.pk}] {field_name}: storage wrote '{saved_name}' "
                            f"instead of '{stored_name}' — row still unresolved"
                        )
                    )
                    missing += 1
                    continue

                uploaded += 1
                self.stdout.write(f"[{template.pk}] uploaded {source.name} -> {stored_name}")

        summary = (
            f"{uploaded} uploaded, {skipped} already present, {missing} unresolved"
            f"{' (dry run)' if dry_run else ''}"
        )
        self.stdout.write(self.style.SUCCESS(summary) if not missing else self.style.WARNING(summary))

    @staticmethod
    def _locate(source_dir: Path, stored_name: str) -> Path | None:
        for basename in candidate_basenames(stored_name):
            candidate = source_dir / basename
            if candidate.is_file():
                return candidate
        return None
