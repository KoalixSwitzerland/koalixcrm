from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email')
