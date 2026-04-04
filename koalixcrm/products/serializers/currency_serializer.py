from rest_framework import serializers

from koalixcrm.products.models.currency import Currency


class CurrencyJSONSerializer(serializers.HyperlinkedModelSerializer):
    shortName = serializers.CharField(source='short_name')

    class Meta:
        model = Currency
        fields = ('id',
                  'description',
                  'shortName',
                  'rounding')
