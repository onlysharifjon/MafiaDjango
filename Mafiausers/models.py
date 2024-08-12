from django.db import models


class  MafiaUserModel(models.Model):
    username = models.CharField(max_length=32, unique=True, default="")
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=4, default="")
    status = models.BooleanField(default=False)
    otp_login = models.CharField(max_length=4, default="")

    def __str__(self) -> str:
        return self.username


class RoomModel(models.Model):
    room_id = models.CharField(max_length=100, unique=True)
    room_users = models.ManyToManyField(MafiaUserModel,null=True)

    def __str__(self):
        return self.room_id
