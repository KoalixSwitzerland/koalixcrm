# -*- coding: utf-8 -*-
"""Print planned backfill counts without writing anything.

Run on a production-sized snapshot BEFORE applying 0005_backfill_party
to see how many new Party/Organization/PartyContact/... rows will be
created. The actual migration is not executed.

Intended for @scaphilo / @Hacont to review prior to deploying #393.
"""
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Print planned Party backfill row counts (read-only, writes nothing)."

    def handle(self, *args, **options):
        from koalixcrm.contacts.backfill import row_count_report

        rows = row_count_report(apps)
        width = max(len(r[0]) for r in rows)
        self.stdout.write(f"{'Entity'.ljust(width)}  {'Expected'.rjust(10)}  {'Current'.rjust(10)}")
        self.stdout.write("-" * (width + 24))
        for label, expected, actual in rows:
            self.stdout.write(
                f"{label.ljust(width)}  {str(expected).rjust(10)}  {str(actual).rjust(10)}"
            )
        self.stdout.write("")
        self.stdout.write(
            "Dry-run only. No rows written. "
            "Apply the migration with `manage.py migrate contacts 0005_backfill_party`."
        )
