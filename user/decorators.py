from django.shortcuts import redirect
from django.urls import reverse


def is_login(func):
    def wrapper(*args, **kwargs):
        if not args[0].session.get('login'):
            return redirect(reverse('auth.phone'))
        return func(*args, **kwargs)
    return wrapper
