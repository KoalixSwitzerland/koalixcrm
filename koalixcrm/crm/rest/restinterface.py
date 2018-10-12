# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer

from koalixcrm.crm.documents.contract import Contract, ContractJSONSerializer
from koalixcrm.crm.product.currency import Currency
from koalixcrm.crm.product.product_type import ProductType
from koalixcrm.crm.product.tax import Tax
from koalixcrm.crm.product.unit import Unit
from koalixcrm.crm.reporting.project import Project, ProjectJSONSerializer
from koalixcrm.crm.reporting.task import Task, TaskSerializer
from koalixcrm.crm.reporting.task_status import TaskStatus
from koalixcrm.crm.rest.currency_rest import CurrencyJSONSerializer
from koalixcrm.crm.rest.product_rest import ProductJSONSerializer
from koalixcrm.crm.rest.tax_rest import TaxJSONSerializer
from koalixcrm.crm.rest.unit_rest import UnitJSONSerializer
from koalixcrm.crm.views.renderer import XSLFORenderer
from koalixcrm.global_support_functions import ConditionalMethodDecorator


class TaskAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, XMLRenderer)
    filter_fields = ('project',)

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(TaskAsJSON, self).dispatch(*args, **kwargs)


class ContractAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Contract.objects.all()
    serializer_class = ContractJSONSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, XMLRenderer)

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(ContractAsJSON, self).dispatch(*args, **kwargs)


class TaskStatusAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = TaskStatus.objects.all()
    serializer_class = TaskSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, XMLRenderer)

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(TaskStatusAsJSON, self).dispatch(*args, **kwargs)


class CurrencyAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows currencies to be viewed.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencyJSONSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, XMLRenderer)

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(CurrencyAsJSON, self).dispatch(*args, **kwargs)


class TaxAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed.
    """
    queryset = Tax.objects.all()
    serializer_class = TaxJSONSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, XMLRenderer)

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(TaxAsJSON, self).dispatch(*args, **kwargs)


class UnitAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows units to be viewed.
    """
    queryset = Unit.objects.all()
    serializer_class = UnitJSONSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, XMLRenderer)

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(UnitAsJSON, self).dispatch(*args, **kwargs)


class ProductAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed.
    """
    queryset = ProductType.objects.all()
    serializer_class = ProductJSONSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, XMLRenderer)

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(ProductAsJSON, self).dispatch(*args, **kwargs)


class ProjectAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectJSONSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, XMLRenderer, XSLFORenderer)
    file_name = "this_is_the_ProjectList.xml"

    @ConditionalMethodDecorator(method_decorator(login_required), settings.KOALIXCRM_REST_API_AUTH)
    def dispatch(self, *args, **kwargs):
        return super(ProjectAsJSON, self).dispatch(*args, **kwargs)
