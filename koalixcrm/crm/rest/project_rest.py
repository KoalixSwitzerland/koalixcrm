# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.crm.reporting.project import Project
from koalixcrm.crm.product.currency import Currency
from koalixcrm.crm.reporting.project_status import ProjectStatus
from koalixcrm.crm.rest.project_status_rest import OptionProjectStatusJSONSerializer
from koalixcrm.crm.rest.currency_rest import CurrencyJSONSerializer
from koalixcrm.djangoUserExtension.rest.user_rest import UserSerializer
from koalixcrm.djangoUserExtension.rest.template_set_rest import OptionTemplateSetJSONSerializer
from koalixcrm.djangoUserExtension.user_extension.template_set import TemplateSet
import koalixcrm


class OptionProjectJSONSerializer(serializers.ModelSerializer):
    projectStatus = OptionProjectStatusJSONSerializer(source='project_status', read_only=True)
    projectManager = UserSerializer(source='project_manager', read_only=True)
    projectName = serializers.CharField(source='project_name', read_only=True)
    defaultCurrency = CurrencyJSONSerializer(source='default_currency', read_only=True)
    defaultTemplateSet = OptionTemplateSetJSONSerializer(source='default_template_set', read_only=True)
    isReportingAllowed = serializers.SerializerMethodField()

    def get_isReportingAllowed(self, obj):
        if obj.is_reporting_allowed():
            return "True"
        else:
            return "False"

    class Meta:
        model = Project
        fields = ('projectStatus',
                  'projectManager',
                  'projectName',
                  'description',
                  'defaultCurrency',
                  'defaultTemplateSet',
                  'isReportingAllowed')


class ProjectJSONSerializer(serializers.ModelSerializer):
    from koalixcrm.crm.rest.task_rest import TaskJSONSerializer
    projectStatus = OptionProjectStatusJSONSerializer(source='project_status')
    projectManager = UserSerializer(source='project_manager', read_only=True)
    projectName = serializers.CharField(source='project_name')
    defaultCurrency = CurrencyJSONSerializer(source='default_currency')
    defaultTemplateSet = OptionTemplateSetJSONSerializer(source='default_template_set')
    isReportingAllowed = serializers.SerializerMethodField()
    tasks = TaskJSONSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('projectStatus',
                  'projectManager',
                  'projectName',
                  'description',
                  'defaultCurrency',
                  'defaultTemplateSet',
                  'isReportingAllowed',
                  'tasks')

    def get_isReportingAllowed(self, obj):
        if obj.is_reporting_allowed():
            return "True"
        else:
            return "False"

    def create(self, validated_data):
        project = Project()
        # Deserialize default currency
        default_currency = validated_data.pop('defaultCurrency')
        if default_currency:
            if default_currency.get('id', None):
                project.default_currency = Currency.objects.get(id=default_currency.get('id', None))
            else:
                project.default_currency = None
        # Deserialize status
        project_status = validated_data.pop('ProjectStatus')
        if project_status:
            if project_status.get('id', None):
                project.project_status = ProjectStatus.objects.get(id=project_status.get('id', None))
            else:
                project.project_status = None
        # Deserialize default template set
        default_template_set = validated_data.pop('defaultTemplateSet')
        if default_template_set:
            if default_template_set.get('id', None):
                project.default_template_set = TemplateSet.objects.get(id=default_template_set.get('id', None))
            else:
                project.default_template_set = None
        project.title = validated_data['title']
        project.description = validated_data['description']
        project.save()
        return project

    def update(self, project, validated_data):
        # Deserialize default currency
        default_currency = validated_data.pop('defaultCurrency')
        if default_currency:
            if default_currency.get('id', project.project):
                project.default_currency = Project.objects.get(id=default_currency.get('id', None))
            else:
                project.default_currency = project.default_currency_id
        else:
            project.default_currency = None
        # Deserialize status
        project_status = validated_data.pop('status')
        if project_status:
            if project_status.get('id', project.status):
                project.project_status = ProjectStatus.objects.get(id=project_status.get('id', None))
            else:
                project.project_status = project.project_status_id
        else:
            project.project_status = None
        # Deserialize default template set
        default_template_set = validated_data.pop('status')
        if default_template_set:
            if default_template_set.get('id', project.default_template_set):
                project.default_template_set = TemplateSet.objects.get(id=default_template_set.get('id', None))
            else:
                project.default_template_set = project.default_template_set_id
        else:
            project.default_template_set = None
        project.title = validated_data['title']
        project.description = validated_data['description']
        project.save()
        return project



