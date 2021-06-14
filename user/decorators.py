from django.shortcuts import redirect
from django.urls import reverse


def session_check(func):
    def wrapper(*args, **kwargs):
        if not args[0].session.get('phone'):
            return redirect(reverse('auth.phone'))
        return func(*args, **kwargs)
    return wrapper
