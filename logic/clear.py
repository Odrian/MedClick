import datetime

from django.utils.timezone import now

from user.models import User, UserCods, Register
from api.models import Session


def all_clear(date):
    date = now()
    UserCods.objects.filter(code_time__date__lt=delta(date, 1)).delete()
    Register.objects.filter(time__date__lt=delta(date, 1)).delete()
    Session.objects.filter(last_activity__lt=delta(date, 190)).delete()


def delta(date, days):
    return date - datetime.timedelta(days=days)
