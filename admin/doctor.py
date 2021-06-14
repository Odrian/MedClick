from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import path, reverse

from admin.decorators import admin_session_check
from doctor.models import Doctor


@admin_session_check
def index(request):
    return render(request, 'admin/base.html', context={'name': 'Доктора'})


def admin_create_doctor(request):
    pass


def admin_edit_doctor(request):
    pass


def admin_delete_doctor(request):
    pass


urlpatterns = [
    path('', index),
    path('create/', admin_create_doctor),
    path('edit/', admin_edit_doctor),
    path('delete/', admin_delete_doctor),
]
