from django.db import models


class User(models.Model):
    Username = models.CharField(max_length=50)
    Email = models.EmailField()
    Password = models.CharField(max_length=60)

