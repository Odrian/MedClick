from django.shortcuts import render
from django.urls import path, include

from .decorators import admin_session_check


@admin_session_check
def index(request):
    return render(request, 'admin/base.html')


urlpatterns = [
    path('', index),
    path('admin/', include('admin.admin'), name='admin.admin'),
    path('doctor/', include('admin.doctor'), name='admin.doctor'),
    path('special/', include('admin.special'), name='admin.special'),
    path('stat/', include('admin.stat')),
]
