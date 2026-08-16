# -*- coding: utf-8 -*-
"""REQ-0019 AC-3 / ADR-0011: recompute OnHandRecord/StockBalance totals from
the immutable StockMovement log and report any drift from the stored
aggregates. Read-only — never writes anything."""
from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Rebuild OnHandRecord/StockBalance totals from the StockMovement log and report mismatches (read-only)."

    def add_arguments(self, parser):
        parser.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")

    def handle(self, *args, **options):
        from koalixcrm.core.models.workspace import Workspace
        from koalixcrm.stock.services.movement_posting import rebuild_from_log

        workspace_id = options["workspace_id"]
        try:
            workspace = Workspace.objects.get(pk=workspace_id)
        except Workspace.DoesNotExist as exc:
            raise CommandError(f"No Workspace with id={workspace_id}") from exc

        report = rebuild_from_log(workspace=workspace)

        if report["consistent"]:
            self.stdout.write(self.style.SUCCESS(
                f"Workspace {workspace_id}: consistent — StockMovement log matches "
                f"OnHandRecord/StockBalance."
            ))
            return

        self.stdout.write(self.style.ERROR(f"Workspace {workspace_id}: INCONSISTENT"))
        for mismatch in report["on_hand_mismatches"]:
            self.stdout.write(
                f"  OnHandRecord {mismatch['key']}: stored={mismatch['stored']} "
                f"expected={mismatch['expected']}"
            )
        for mismatch in report["balance_mismatches"]:
            self.stdout.write(
                f"  StockBalance {mismatch['key']}: stored={mismatch['stored']} "
                f"expected={mismatch['expected']}"
            )
        raise CommandError("Consistency check failed; see mismatches above.")
