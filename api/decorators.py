from django.http import JsonResponse
from django.utils.timezone import now

from .models import Session


def session_check(func):
    def wrapper(*args, **kwargs):
        key = args[0].POST.get('session_key')
        session = Session.objects.filter(key=key)
        if len(session) == 0:
            return JsonResponse({'info':'session_error', 'path':'auth.phone'})
        session = session[0]
        session.last_activity = now()
        session.save()
        return func(*args, phone=session.phone, **kwargs)
    return wrapper


def convert_input(func):
    def wrapper(*args, **kwargs):
        data = str(args[0].body).split('&')
        data2 = {}
        for x in data:
            x = x.replace('%98', '&').split('=')
            if len(x) != 2:
                return func(*args, post={}, **kwargs)
            data2[x[0].replace('%99', '=')] = x[1].replace('%99', '=')
        return func(*args, post=data2, **kwargs)
    return wrapper
