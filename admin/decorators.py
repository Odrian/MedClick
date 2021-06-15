from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from .models import Admin

def admin_session_check(func):
    def wrapper(*args, **kwargs):
        phone = args[0].session.get('phone', '')
        try:
            Admin.objects.get(user__phone=phone)
        except Admin.DoesNotExist:
            return redirect(reverse('auth.phone'))
        return func(*args, **kwargs)
    return wrapper
