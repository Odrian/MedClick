from django.db import models
from user.models import User


class TextChat(models.Model):
    members = models.ManyToManyField(User)
    objects = models.Manager
