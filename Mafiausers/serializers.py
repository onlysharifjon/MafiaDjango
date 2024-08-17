from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers



class LoginSerializer(Serializer):
    email = serializers.EmailField()


from rest_framework.serializers import ModelSerializer
from .models import *

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
        fields = ['otp', ]


class VerifyLoginSerializer(ModelSerializer):
    class Meta:
        model = MafiaUserModel
        fields = ['otp_login', ]


class RoomJoinSerializer(Serializer):
    user_id = serializers.IntegerField()
    room_id = serializers.CharField(max_length=255)



class StartGameSerializer(ModelSerializer):
    class Meta:
        model = RoomModel
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PariticipantModel
        fields = ['user_id', 'role', 'is_dead']


class GameInformationSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = GameInformationModel
        fields = ['id', 'room', 'participants']

