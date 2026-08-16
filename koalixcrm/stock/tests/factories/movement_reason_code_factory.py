# -*- coding: utf-8 -*-
import factory

from koalixcrm.stock.models.movement_reason_code import MovementReasonCode


class StandardMovementReasonCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MovementReasonCode
        django_get_or_create = ('code',)

    code = factory.Sequence(lambda n: f"REASON-{n}")
    label_de = "Standardgrund"
    label_en = "Standard Reason"
    applies_to_business_steps = []
