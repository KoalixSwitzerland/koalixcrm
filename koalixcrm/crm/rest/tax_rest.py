from rest_framework import serializers

from koalixcrm.crm.product.tax import Tax


class OptionTaxJSONSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    description = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = Tax
        fields = ('id',
                  'description')


class TaxJSONSerializer(serializers.HyperlinkedModelSerializer):
    rate = serializers.CharField(source='tax_rate')
    description = serializers.CharField(source='name')

    class Meta:
        model = Tax
        fields = ('id',
                  'rate',
                  'description')
