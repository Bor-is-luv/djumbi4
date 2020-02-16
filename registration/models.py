from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    avatar = models.ImageField()
