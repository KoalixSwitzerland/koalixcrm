from rest_framework import serializers
from koalixcrm.djangoUserExtension.models.user_extension import UserExtension
from koalixcrm.products.serializers.currency_serializer import CurrencyJSONSerializer
from koalixcrm.djangoUserExtension.serializers.template_set_rest import TemplateSetJSONSerializer


class OptionUserExtensionJSONSerializer(serializers.HyperlinkedModelSerializer):
    default_template_set = TemplateSetJSONSerializer()
    default_currency = CurrencyJSONSerializer()

    class Meta:
        model = UserExtension
        fields = ('id',
                  'user',
                  'default_template_set',
                  'default_currency')
