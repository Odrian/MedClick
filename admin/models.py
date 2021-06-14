from django.db import models

from user.models import User


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    objects = models.Manager()
