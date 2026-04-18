# -*- coding: utf-8 -*-
"""Pre-cutover verification for the Party data migration (issue #395).

Run this against a COPY of the production DB after applying
v2.0.0 migrations up to `contacts.0005_backfill_party` but BEFORE
the destructive migrations that drop the legacy tables. If it exits
zero, v2.0.0 is safe to apply. If it exits non-zero, see the output +
`docs/migration-v1.14.0-to-v2.0.0.md` for remediation.

The same logic runs non-interactively inside migration
`contacts.0006_verify_ready_for_cutover` — this command is just the
operator-friendly view.
"""
import sys

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Verify the Party data migration is ready for the destructive "
        "v2.0.0 cutover. Exits non-zero on any failed invariant."
    )

    def handle(self, *args, **options):
        from koalixcrm.contacts.backfill_verify import verify_ready_for_cutover

        checks = verify_ready_for_cutover(apps, raise_on_failure=False)

        width = max(len(c.name) for c in checks)
        self.stdout.write(
            f"{'Invariant'.ljust(width)}  {'Legacy'.rjust(8)}  "
            f"{'New'.rjust(8)}  Delta  Status"
        )
        self.stdout.write("-" * (width + 36))
        for c in checks:
            status = 'OK' if c.passed else 'FAIL'
            marker = '' if c.passed else ' !!'
            self.stdout.write(
                f"{c.name.ljust(width)}  {str(c.legacy_count).rjust(8)}  "
                f"{str(c.new_count).rjust(8)}  {c.delta:+5d}  {status}{marker}"
            )

        failed = [c for c in checks if not c.passed]
        if failed:
            self.stderr.write("")
            self.stderr.write(self.style.ERROR(
                f"{len(failed)} invariant(s) failed. Fix remediation hints:"
            ))
            for c in failed:
                self.stderr.write(f"\n  ✗ {c.name}")
                self.stderr.write(f"    hint: {c.hint}")
            self.stderr.write("")
            self.stderr.write(self.style.ERROR(
                "Do NOT deploy v2.0.0 to production until every invariant is green. "
                "See docs/migration-v1.14.0-to-v2.0.0.md "
                "#upgrading-contacts-data-to-the-party-model"
            ))
            sys.exit(1)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            "All invariants hold. Safe to run the destructive v2.0.0 migrations."
        ))
