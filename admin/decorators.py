from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.models import AdminSession


def admin_session_check(func):
    @api_view(['POST'])
    def wrapper(*args, **kwargs):
        key = args[0].POST.get('session_key')
        try:
            AdminSession.objects.get(key=key)
        except AdminSession.DoesNotExist:
            return JsonResponse({'info': 'session_error'})
        return func(*args, **kwargs)
    return wrapper
