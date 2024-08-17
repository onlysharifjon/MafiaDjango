from django.db import models

CHOICES = [
    ("don","Don"),
    ("doc",'Doctor'),
    ("kom","Komissar"),
    ("people","Oddiy aholi"),
    ("mafia","Mafia")
]


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
    room_users = models.ManyToManyField(MafiaUserModel)

    def __str__(self):
        return self.room_id


class PariticipantModel(models.Model):
    user_id = models.ForeignKey(MafiaUserModel, on_delete=models.CASCADE)
    role = models.CharField(choices=CHOICES, max_length=25)
    is_dead = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user_id)


class GameInformationModel(models.Model):
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    participants = models.ManyToManyField(PariticipantModel)

    def __str__(self) -> str:
        return str(self.id)


