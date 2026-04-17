# -*- coding: utf-8 -*-
"""Re-check backfill invariants AFTER applying 0005_backfill_party.

Runs the same `{label: (expected, actual)}` report as the dry-run and
exits non-zero if any row's `expected != actual`. Intended to be run
against staging and production immediately after the migration deploys.
"""
import sys

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Verify Party backfill invariants. Exits non-zero if any row mismatches."

    def handle(self, *args, **options):
        from koalixcrm.contacts.backfill import row_count_report

        rows = row_count_report(apps)
        width = max(len(r[0]) for r in rows)
        mismatches = []

        self.stdout.write(f"{'Entity'.ljust(width)}  {'Expected'.rjust(10)}  {'Actual'.rjust(10)}  Delta")
        self.stdout.write("-" * (width + 32))
        for label, expected, actual in rows:
            delta = actual - expected
            marker = '' if delta == 0 else ' !!'
            self.stdout.write(
                f"{label.ljust(width)}  {str(expected).rjust(10)}  {str(actual).rjust(10)}  "
                f"{delta:+d}{marker}"
            )
            if delta != 0:
                mismatches.append((label, expected, actual, delta))

        if mismatches:
            self.stderr.write("")
            self.stderr.write(self.style.ERROR(
                f"{len(mismatches)} invariant(s) failed — inspect above."
            ))
            sys.exit(1)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("All backfill invariants hold."))
