# -*- coding: utf-8 -*-
"""Bumps `BillOfMaterials.version` whenever one of its `BomItem` rows is
created, changed or removed (ADR-0014). The BOM-explosion snapshot table
(`stock.BillOfMaterialsExplosion`) pins the version it was computed
against; the pick-time path recomputes synchronously when the current
version has moved past the pinned one. Registered from
`koalixcrm.products.apps.ProductsConfig.ready()`."""
from __future__ import annotations

from django.db.models import F
from django.db.models.signals import post_delete, post_save

from koalixcrm.products.models.bom_item import BomItem


def _bump_version(sender, instance, **kwargs) -> None:
    from koalixcrm.products.models.bill_of_materials import BillOfMaterials

    BillOfMaterials.objects.filter(pk=instance.bill_of_materials_id).update(version=F("version") + 1)


def register_bom_version_signals() -> None:
    post_save.connect(_bump_version, sender=BomItem, dispatch_uid="bom_version_bump_save")
    post_delete.connect(_bump_version, sender=BomItem, dispatch_uid="bom_version_bump_delete")
