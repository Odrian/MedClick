from django.db import models
from user.models import User


class TextChat(models.Model):
    members = models.ManyToManyField(User)
    objects = models.Manager

class ChatCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(TextChat, on_delete=models.CASCADE)
    check = models.BooleanField(default=False)
