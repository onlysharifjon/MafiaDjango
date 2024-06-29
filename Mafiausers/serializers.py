from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers


class LoginSerializer(Serializer):
    email = serializers.EmailField()
