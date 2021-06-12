from django.http import JsonResponse
from django.urls import path

from .decorators import admin_session_check


@admin_session_check
def admin_get_stats(request):
    return JsonResponse({'info': 'it_dont_work'})


urlpatterns = [
    path('', admin_get_stats),
]
