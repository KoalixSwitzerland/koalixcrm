# -*- coding: utf-8 -*-
"""
Mixin adding a ``GET /{model}/{id}/nested/`` detail action.

Subclasses set ``nested_serializer_class`` to the deeply-nested serializer
they want to expose. The action returns the same object ``retrieve`` would
but rendered through the nested shape the PDF worker consumes.

Kept as a separate action (instead of swapping the default serializer) so that
existing shallow clients continue to work and so that write operations still
flow through the simpler flat serializers.
"""
from rest_framework.decorators import action
from rest_framework.response import Response


class NestedDetailMixin:
    nested_serializer_class = None

    @action(detail=True, methods=["get"], url_path="nested", url_name="nested")
    def nested(self, request, pk=None, **kwargs):
        serializer_class = self.nested_serializer_class
        if serializer_class is None:
            raise NotImplementedError(
                f"{type(self).__name__} must set nested_serializer_class"
            )
        instance = self.get_object()
        serializer = serializer_class(
            instance, context=self.get_serializer_context()
        )
        return Response(serializer.data)
