from django.http import JsonResponse
from django.utils.timezone import now

from .models import Session


def session_check(func):
    def wrapper(*args, **kwargs):
        key = args[0].POST.get('session')
        session = Session.objects.filter(key=key)
        if len(session) == 0:
            return JsonResponse({'info':'session_error', 'path':'auth.phone'})
        session = session[0]
        session.last_activity = now()
        session.save()
        return func(*args, phone=session.phone, **kwargs)
    return wrapper
