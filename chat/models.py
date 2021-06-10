from django.db import models
from user.models import User


class Chat(models.Model):
#    members = models.IntegerField(default=0)
#    file_count = models.IntegerField(default=0)
    objects = models.Manager

class Checker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    check = models.BooleanField(default=False)
    objects = models.Manager
