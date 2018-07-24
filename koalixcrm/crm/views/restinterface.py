# -*- coding: utf-8 -*-
from koalixcrm.crm.product.product import Product, ProductJSONSerializer

from koalixcrm.crm.product.unit import Unit, UnitJSONSerializer

from koalixcrm.crm.product.tax import Tax, TaxJSONSerializer
from rest_framework import viewsets

from koalixcrm.crm.product.currency import CurrencyJSONSerializer, Currency
from koalixcrm.crm.reporting.task import Task, TaskJSONSerializer
from koalixcrm.crm.reporting.taskstatus import TaskStatus, TaskStatusJSONSerializer
from koalixcrm.crm.documents.contract import Contract, ContractJSONSerializer
from koalixcrm.crm.reporting.project import Project, ProjectJSONSerializer


class TaskAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Task.objects.all()
    serializer_class = TaskJSONSerializer
    filter_fields = ('project',)


class ContractAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Contract.objects.all()
    serializer_class = ContractJSONSerializer


class TaskStatusAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusJSONSerializer


class CurrencyAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows currencies to be viewed.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencyJSONSerializer


class TaxAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed.
    """
    queryset = Tax.objects.all()
    serializer_class = TaxJSONSerializer


class UnitAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows units to be viewed.
    """
    queryset = Unit.objects.all()
    serializer_class = UnitJSONSerializer


class ProductAsJSON(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed.
    """
    queryset = Product.objects.all()
    serializer_class = ProductJSONSerializer


class ProjectAsJSON(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectJSONSerializer
