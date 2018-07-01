# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.template.base import logger
from django.utils.translation import ugettext as _
from rest_framework import serializers


class Unit(models.Model):
    description = models.CharField(verbose_name=_("Description"),
                                   max_length=100)
    short_name = models.CharField(verbose_name=_("Displayed Name After Quantity In The Position"),
                                  max_length=3)
    is_a_fraction_of = models.ForeignKey('self',
                                         blank=True,
                                         null=True,
                                         verbose_name=_("Is A Fraction Of"))
    fraction_factor_to_next_higher_unit = models.DecimalField(verbose_name=_("Factor Between This And Next Higher Unit"),
                                                              max_digits=20,
                                                              decimal_places=10,
                                                              blank=True,
                                                              null=True)

    def __str__(self):
        return self.short_name

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')


class OptionUnit(admin.ModelAdmin):
    list_display = ('id', 'description', 'short_name', 'is_a_fraction_of', 'fraction_factor_to_next_higher_unit')
    fieldsets = (('', {'fields': ('description', 'short_name', 'is_a_fraction_of', 'fraction_factor_to_next_higher_unit')}),)
    allow_add = True


class UnitTransform(models.Model):
    from_unit = models.ForeignKey('Unit', verbose_name=_("From Unit"), related_name="db_reltransfromfromunit")
    to_unit = models.ForeignKey('Unit', verbose_name=_("To Unit"), related_name="db_reltransfromtounit")
    product = models.ForeignKey('Product', verbose_name=_("Product"))
    factor = models.IntegerField(verbose_name=_("Factor between From and To Unit"), blank=True, null=True)

    def transform(self, unit):
        if (self.from_unit == unit):
            return self.to_unit
        else:
            return unit

    def __str__(self):
        return "From " + self.from_unit.short_name + " to " + self.to_unit.short_name

    class Meta:
        app_label = "crm"
        verbose_name = _('Unit Transfrom')
        verbose_name_plural = _('Unit Transfroms')


class ProductUnitTransform(admin.TabularInline):
    model = UnitTransform
    extra = 1
    classes = ['collapse']
    fieldsets = (
        ('', {
            'fields': ('from_unit', 'to_unit', 'factor',)
        }),
    )
    allow_add = True


class UnitMinimalJSONSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    description = serializers.CharField(read_only=True)
    shortName = serializers.CharField(source='short_name', read_only=True)

    class Meta:
        model = Unit
        fields = ('id',
                  'description',
                  'shortName')


class UnitJSONSerializer(serializers.HyperlinkedModelSerializer):
    shortName = serializers.CharField(source='short_name')
    description = serializers.CharField()
    isFractionOf = UnitMinimalJSONSerializer(source='is_a_fraction_of',
                                             allow_null=True)
    fractionFactor = serializers.DecimalField(source='fraction_factor_to_next_higher_unit',
                                              max_digits=20,
                                              decimal_places=10,
                                              required=False,
                                              allow_null=True)

    class Meta:
        model = Unit
        fields = ('id',
                  'description',
                  'shortName',
                  'isFractionOf',
                  'fractionFactor')
        depth = 1

    def create(self, validated_data):
        unit = Unit()
        unit.description = validated_data['description']
        unit.short_name = validated_data['short_name']
        if 'fraction_factor_to_next_higher_unit' in validated_data:
            unit.fraction_factor_to_next_higher_unit = validated_data['fraction_factor_to_next_higher_unit']

        parent_unit = validated_data.pop('is_a_fraction_of')
        if parent_unit:
            if parent_unit.get('id', None):
                unit.is_a_fraction_of = Unit.objects.get(id=parent_unit.get('id', None))
            else:
                unit.is_a_fraction_of = None
        unit.save()
        return unit

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.short_name = validated_data.get('short_name', instance.short_name)

        parent_unit = validated_data.pop('is_a_fraction_of')
        if parent_unit:
            if parent_unit.get('id', instance.is_a_fraction_of_id):
                instance.is_a_fraction_of = Unit.objects.get(id=parent_unit.get('id', None))
            else:
                instance.is_a_fraction_of = instance.is_a_fraction_of_id
        else:
            instance.is_a_fraction_of = None
        instance.fraction_factor_to_next_higher_unit = validated_data.get('fraction_factor_to_next_higher_unit', instance.fraction_factor_to_next_higher_unit)
        instance.save()

        return instance


