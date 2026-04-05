# -*- coding: utf-8 -*-
from koalixcrm.shared.base_model_view_set import BaseModelViewSet
from koalixcrm.reporting.models.generic_project_link import GenericProjectLink
from koalixcrm.reporting.serializers.generic_project_link_serializer import GenericProjectLinkJSONSerializer


class GenericProjectLinkViewSet(BaseModelViewSet):
    queryset = GenericProjectLink.objects.all()
    serializer_class = GenericProjectLinkJSONSerializer
