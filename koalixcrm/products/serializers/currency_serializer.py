from rest_framework import serializers

from koalixcrm.products.models.currency import Currency


class CurrencyJSONSerializer(serializers.HyperlinkedModelSerializer):
    short_name = serializers.CharField()

    class Meta:
        model = Currency
        fields = ('id',
                  'description',
                  'short_name',
                  'rounding')
