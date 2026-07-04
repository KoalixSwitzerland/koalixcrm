# -*- coding: utf-8 -*-
"""`AttributeValidationRule` — ADR-0020 cross-field/conditional attribute
validation, stored as serializable data and bound to an `AttributeSet`
(the "natural carrier" of attribute metadata per ADR-0020). Both the
Python backend (authoritative, on every write) and the closed-source
TypeScript frontend (live-form UX) evaluate the *same* serialized
`condition`/`then` payload — see
`koalixcrm.products.services.attribute_rule_engine.evaluate_rules` for the
Python evaluator and `tests/products/fixtures/attribute_rule_conformance.json`
for the shared conformance fixtures ADR-0020 requires.

ADR-0020 explicitly defers the concrete rule grammar to a follow-up ADR;
this is a pragmatic seed format (condition/then, a handful of operators)
scoped to the ADR-0004/0018/0019 use cases at hand. Escalate to
`dev-kxcrm-architect` before extending the operator set."""
from __future__ import annotations

from django.db import models
from django.utils.translation import gettext as _

from koalixcrm.core.models.workspace_scoped import WorkspaceScopedModel


class AttributeValidationRule(WorkspaceScopedModel):
    id = models.BigAutoField(primary_key=True)
    attribute_set = models.ForeignKey(
        "AttributeSet",
        on_delete=models.CASCADE,
        verbose_name=_("Attribute Set"),
        related_name="validation_rules",
    )
    key = models.SlugField(verbose_name=_("Key"), max_length=100)
    name = models.CharField(verbose_name=_("Name"), max_length=200)
    order = models.PositiveIntegerField(verbose_name=_("Order"), default=0)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    condition = models.JSONField(
        verbose_name=_("Condition"),
        help_text=_('e.g. {"attribute": "gloss_level", "op": "eq", "value": "matt"}'),
    )
    then = models.JSONField(
        verbose_name=_("Then"),
        help_text=_(
            'e.g. {"attribute": "voc_content", "requirement": "required"} or '
            '{"attributes": ["a", "b"], "requirement": "mutually_exclusive"}'
        ),
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        app_label = "products"
        db_table = "products_attributevalidationrule"
        verbose_name = _("Attribute Validation Rule")
        verbose_name_plural = _("Attribute Validation Rules")
        ordering = ["attribute_set_id", "order"]
        constraints = [
            models.UniqueConstraint(fields=["attribute_set", "key"], name="unique_attribute_validation_rule_key"),
        ]
