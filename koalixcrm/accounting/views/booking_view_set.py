# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.accounting.models import Booking
from koalixcrm.accounting.serializers.booking_serializer import BookingJSONSerializer


class BookingViewSet(BaseModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingJSONSerializer
