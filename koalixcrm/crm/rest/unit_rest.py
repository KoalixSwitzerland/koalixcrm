from rest_framework import serializers

from koalixcrm.crm.product.unit import Unit


class OptionUnitJSONSerializer(serializers.HyperlinkedModelSerializer):
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
    isFractionOf = OptionUnitJSONSerializer(source='is_a_fraction_of',
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
        instance.fraction_factor_to_next_higher_unit = validated_data.get('fraction_factor_to_next_higher_unit',
                                                                          instance.fraction_factor_to_next_higher_unit)
        instance.save()

        return instance
