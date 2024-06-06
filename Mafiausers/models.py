from django.db import models


# Create your models here.


class MafiauserModel(models.Model):
    username = models.CharField(unique=True, max_length=16)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class VerficatorModel(models.Model):
    email = models.ForeignKey(MafiauserModel, on_delete=models.CASCADE)
    verfication_code = models.CharField(max_length=6, default='001001')
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)
