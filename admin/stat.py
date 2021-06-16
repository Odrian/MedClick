from django.urls import path

from .decorators import admin_session_check


from django.conf import settings
from django.http import HttpResponse
@admin_session_check
def admin_get_stats(request):
    with open(settings.LOGFILE, 'r') as file:
        return HttpResponse('''<style>
        body {font-family: monospace;}
        div {margin: 2px 0 5px}
        </style>''' + '<div>' + '</div><div>'.join(file.readlines()[::-1]) + '</div>')


urlpatterns = [
    path('', admin_get_stats),
]
