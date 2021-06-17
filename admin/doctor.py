from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import path, reverse

from admin.decorators import admin_session_check
from doctor.models import Doctor


@admin_session_check
def index(request):
    return render(request, 'admin/base.html', context={
        'path1': 'Доктора', 'doctors': [], 'length': len([])})


urlpatterns = [
    path('', index),
]
