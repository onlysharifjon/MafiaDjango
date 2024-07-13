from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers


class LoginSerializer(Serializer):
    email = serializers.EmailField()


from rest_framework.serializers import ModelSerializer
from .models import MafiaUserModel


class MafiaModelSerializer(ModelSerializer):
    class Meta:
        model = MafiaUserModel
        fields = "__all__"


class RegisterSRL(ModelSerializer):
    class Meta:
        model = MafiaUserModel
        fields = ['email', 'username']

class VerifySerializer(ModelSerializer):
    class Meta:
        model = MafiaUserModel
        fields = ['otp',]