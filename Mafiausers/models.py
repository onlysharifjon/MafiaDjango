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
    is_started = models.BooleanField(default=False)
    room_id = models.CharField(max_length=100, unique=True)
    room_users = models.ManyToManyField(MafiaUserModel)

    def __str__(self):
        return self.room_id
CHOICES = [
    ("Manyak","Manyak"),
    ("Doctor",'Doctor'),
    ("Komissar","Komissar"),
    ("Oddiy aholi","Oddiy aholi"),
    ("Mafia","Mafia"),
    ("Oyinchi","Oyinchi")
    

]
class RoomRole(models.Model):
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    user = models.ForeignKey(MafiaUserModel, on_delete=models.CASCADE)
    role = models.CharField(max_length=22, choices=CHOICES)
    is_died = models.BooleanField(default=False)

    def __str__(self):
        return self.role




