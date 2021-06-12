import django
from django.db import models


class Session(models.Model):
    key = models.CharField(max_length=16, primary_key=True)
    phone = models.CharField(max_length=16)
    last_activity = models.DateField(default=django.utils.timezone.now)
    objects = models.Manager()

class AdminSession(models.Model):
    key = models.CharField(max_length=16, primary_key=True)
    objects = models.Manager()
