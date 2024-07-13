from django.db import models


# Create your models here.


# class MafiauserModel(models.Model):
#     username = models.CharField(unique=True, max_length=16)
#     email = models.EmailField(unique=True)
#
#     def __str__(self):
#         return self.username


class MafiaUserModel(models.Model):
    username = models.CharField(max_length=32, unique=True, default="")
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=4, default="")
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
