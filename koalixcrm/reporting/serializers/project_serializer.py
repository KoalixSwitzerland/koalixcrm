# -*- coding: utf-8 -*-
from rest_framework import serializers
from koalixcrm.reporting.models.project import Project
from koalixcrm.products.models.currency import Currency
from koalixcrm.reporting.models.project_status import ProjectStatus
from koalixcrm.reporting.serializers.project_status_serializer import OptionProjectStatusJSONSerializer
from koalixcrm.products.serializers.currency_serializer import CurrencyJSONSerializer
from koalixcrm.djangoUserExtension.serializers.user_rest import UserSerializer
from koalixcrm.djangoUserExtension.serializers.template_set_rest import OptionTemplateSetJSONSerializer
from koalixcrm.djangoUserExtension.models.template_set import TemplateSet
import koalixcrm


class OptionProjectJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    project_status = OptionProjectStatusJSONSerializer(read_only=True)
    project_manager = UserSerializer(read_only=True)
    project_name = serializers.CharField(read_only=True)
    default_currency = CurrencyJSONSerializer(read_only=True)
    default_template_set = OptionTemplateSetJSONSerializer(read_only=True)
    is_reporting_allowed = serializers.SerializerMethodField()

    def get_is_reporting_allowed(self, obj):
        if obj.is_reporting_allowed():
            return "True"
        else:
            return "False"

    class Meta:
        model = Project
        fields = ('id',
                  'project_status',
                  'project_manager',
                  'project_name',
                  'description',
                  'default_currency',
                  'default_template_set',
                  'is_reporting_allowed')


class ProjectJSONSerializer(serializers.ModelSerializer):
    project_status = OptionProjectStatusJSONSerializer()
    project_manager = UserSerializer(read_only=True)
    project_name = serializers.CharField()
    default_currency = CurrencyJSONSerializer()
    default_template_set = OptionTemplateSetJSONSerializer()
    is_reporting_allowed = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id',
                  'project_status',
                  'project_manager',
                  'project_name',
                  'description',
                  'default_currency',
                  'default_template_set',
                  'is_reporting_allowed',
                  'tasks')

    def get_tasks(self, obj):
        from koalixcrm.reporting.serializers.task_serializer import TaskJSONSerializer
        tasks = obj.tasks.all()
        return TaskJSONSerializer(tasks, many=True, context=self.context).data

    def get_is_reporting_allowed(self, obj):
        if obj.is_reporting_allowed():
            return "True"
        else:
            return "False"

    def create(self, validated_data):
        project = Project()
        # Deserialize default currency
        default_currency = validated_data.pop('default_currency')
        if default_currency:
            if default_currency.get('id', None):
                project.default_currency = Currency.objects.get(id=default_currency.get('id', None))
            else:
                project.default_currency = None
        # Deserialize status
        project_status = validated_data.pop('project_status')
        if project_status:
            if project_status.get('id', None):
                project.project_status = ProjectStatus.objects.get(id=project_status.get('id', None))
            else:
                project.project_status = None
        # Deserialize default template set
        default_template_set = validated_data.pop('default_template_set')
        if default_template_set:
            if default_template_set.get('id', None):
                project.default_template_set = TemplateSet.objects.get(id=default_template_set.get('id', None))
            else:
                project.default_template_set = None
        project.project_name = validated_data['project_name']
        project.description = validated_data['description']
        # Set last_modified_by from request user
        request = self.context.get('request')
        if request and request.user:
            project.project_manager = request.user
            project.last_modified_by = request.user
        project.save()
        return project

    def update(self, project, validated_data):
        # Deserialize default currency
        default_currency = validated_data.pop('default_currency')
        if default_currency:
            if default_currency.get('id', None):
                project.default_currency = Currency.objects.get(id=default_currency.get('id', None))
            else:
                project.default_currency = project.default_currency_id
        else:
            project.default_currency = None
        # Deserialize status
        project_status = validated_data.pop('project_status')
        if project_status:
            if project_status.get('id', project.project_status):
                project.project_status = ProjectStatus.objects.get(id=project_status.get('id', None))
            else:
                project.project_status = project.project_status_id
        else:
            project.project_status = None
        # Deserialize default template set
        default_template_set = validated_data.pop('default_template_set')
        if default_template_set:
            if default_template_set.get('id', project.default_template_set):
                project.default_template_set = TemplateSet.objects.get(id=default_template_set.get('id', None))
            else:
                project.default_template_set = project.default_template_set_id
        else:
            project.default_template_set = None
        project.project_name = validated_data.get('project_name', project.project_name)
        project.description = validated_data.get('description', project.description)
        project.save()
        return project
