# -*- coding: utf-8 -*-
from __future__ import annotations

from rest_framework import serializers

from koalixcrm.stock.models.choices import ReservationKind, ReservationLifecycleStatus
from koalixcrm.stock.models.rental_assignment import RentalAssignment


class RentalAssignmentJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalAssignment
        fields = ('id',
                  'serial_unit',
                  'on_hand_record',
                  'reservation',
                  'party',
                  'document_type',
                  'document_id',
                  'rental_start',
                  'return_due_date',
                  'returned_at',
                  'status',
                  'condition_at_return',
                  'date_of_creation',
                  'last_modification')
        read_only_fields = ('date_of_creation', 'last_modification')

    def validate(self, attrs):
        reservation = attrs.get('reservation') or (self.instance.reservation if self.instance else None)
        if reservation is not None:
            if reservation.kind != ReservationKind.RENTAL:
                raise serializers.ValidationError("reservation must have kind = RENTAL.")
            if reservation.status != ReservationLifecycleStatus.FULFILLED:
                raise serializers.ValidationError(
                    "reservation must be FULFILLED before a RentalAssignment can reference it."
                )
        return attrs
