# -*- coding: utf-8 -*-
"""`BillOfMaterialsExplosion` — a precomputed, flattened BOM-explosion
snapshot row (ADR-0014). Populated by `services/bom_explosion.py::explode()`
(a plain, synchronous service function; no async recompute-on-BOM-change
path is built today — org ADR-0002 §2.4). Soft depth limits:
depth <= 10 (warn), depth <= 20 (hard reject, `PREASSEMBLE` recommended)."""
from __future__ import annotations

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class BillOfMaterialsExplosion(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    bill_of_materials = models.ForeignKey("products.BillOfMaterials",
                                          on_delete=models.CASCADE,
                                          verbose_name=_("Bill of Materials"),
                                          related_name="explosion_rows")
    bom_version = models.IntegerField(verbose_name=_("BOM Version"))
    depth = models.IntegerField(verbose_name=_("Depth"))
    bom_item = models.ForeignKey("products.BomItem",
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Leaf BOM Item"),
                                 related_name="explosion_rows")
    effective_qty = models.DecimalField(verbose_name=_("Effective Quantity"),
                                        max_digits=18,
                                        decimal_places=4,
                                        validators=[MinValueValidator(Decimal("0"))])
    uom = models.ForeignKey("core.Unit",
                            on_delete=models.PROTECT,
                            verbose_name=_("Unit of Measure"))
    computed_at = models.DateTimeField(verbose_name=_("Computed At"), auto_now=True)

    def __str__(self) -> str:
        return f"{self.bill_of_materials_id}@v{self.bom_version}: {self.bom_item_id} x {self.effective_qty}"

    class Meta:
        app_label = "stock"
        db_table = "stock_billofmaterialsexplosion"
        verbose_name = _("Bill of Materials Explosion")
        verbose_name_plural = _("Bill of Materials Explosions")
        ordering = ["bill_of_materials_id", "depth", "id"]
        indexes = [
            models.Index(fields=["workspace", "bill_of_materials", "bom_version"],
                         name="idx_bomexplosion_bom_version"),
        ]
