from rest_framework import serializers

from koalixcrm.core.models.tax import Tax


class OptionTaxJSONSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Tax
        fields = ('id',
                  'name')


class TaxJSONSerializer(serializers.ModelSerializer):
    """Core-level Tax serializer. Accounting linkage (activa/passiva accounts)
    is owned by `accounting.TaxAccountAssignment` since CR-2c and surfaced
    through accounting-side serializers only."""
    tax_rate = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = Tax
        fields = ('id',
                  'tax_rate',
                  'name')

    def create(self, validated_data):
        tax = Tax()
        tax.tax_rate = validated_data['tax_rate']
        tax.name = validated_data['name']
        tax.save()
        return tax

    def update(self, instance, validated_data):
        instance.tax_rate = validated_data['tax_rate']
        instance.name = validated_data['name']
        instance.save()
        return instance
