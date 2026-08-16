# -*- coding: utf-8 -*-
"""`GoodsReceipt` — the process aggregate for a (possibly multi-session)
goods-receipt process (ADR-0017, UC-0010). Header entity; the DRAFT ->
IN_PROGRESS -> COMPLETED/CANCELLED state machine is enforced in
`services/goods_receipt_workflow.py`, not here — the model layer only
carries the state, never transitions it directly (mirrors the
`StockReservation`/`ProductionOrder` pattern: services own transitions)."""
from __future__ import annotations

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel
from koalixcrm.stock.models.choices import GoodsReceiptStatus


class GoodsReceipt(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    supplier_party = models.ForeignKey("contacts.Party",
                                       on_delete=models.PROTECT,
                                       verbose_name=_("Supplier"),
                                       related_name="goods_receipts")
    external_doc_ref = models.CharField(verbose_name=_("External Document Reference"),
                                        max_length=200,
                                        null=True,
                                        blank=True,
                                        help_text=_("Supplier's delivery note number."))
    received_at = models.DateTimeField(verbose_name=_("Received At"), default=timezone.now)
    status = models.CharField(verbose_name=_("Status"),
                              max_length=16,
                              choices=GoodsReceiptStatus.choices,
                              default=GoodsReceiptStatus.DRAFT)
    notes = models.TextField(verbose_name=_("Notes"), null=True, blank=True)
    created_by = models.ForeignKey("auth.User",
                                   on_delete=models.SET_NULL,
                                   verbose_name=_("Created By"),
                                   related_name="goods_receipts",
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)

    def __str__(self) -> str:
        return f"GoodsReceipt#{self.pk} ({self.external_doc_ref or '-'}) {self.status}"

    class Meta:
        app_label = "stock"
        db_table = "stock_goodsreceipt"
        verbose_name = _("Goods Receipt")
        verbose_name_plural = _("Goods Receipts")
        ordering = ["-received_at", "-id"]
        indexes = [
            models.Index(fields=["workspace", "status"], name="idx_goodsreceipt_status"),
            models.Index(fields=["workspace", "supplier_party"], name="idx_goodsreceipt_supplier"),
        ]
