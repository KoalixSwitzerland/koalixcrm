# -*- coding: utf-8 -*-
"""ADR-0014: thin Celery task shell around
`services/bom_explosion.explode()`, following the existing SQS-backed
Celery app (`koalixcrm_microservices/celery_app.py`). This module adds no
new infrastructure — it reuses the already-configured `app` instance. Every
synchronous call site (admin actions, the pick-time staleness check in
`services/bom_explosion.get_or_recompute_explosion`) calls `explode()`
directly; this task is an optional async entry point for callers that want
to recompute a BOM-explosion snapshot out-of-band (e.g. a bulk BOM import)
without blocking the request/response cycle."""
from __future__ import annotations

from koalixcrm_microservices.celery_app import app


@app.task(name="koalixcrm.stock.recompute_bom_explosion")
def recompute_bom_explosion_task(bill_of_materials_id: int) -> None:
    from koalixcrm.products.models.bill_of_materials import BillOfMaterials
    from koalixcrm.stock.services.bom_explosion import explode

    bill_of_materials = BillOfMaterials.objects.get(pk=bill_of_materials_id)
    explode(bill_of_materials)
