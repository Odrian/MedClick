from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import path, reverse

from doctor.models import Specialization

from .decorators import admin_session_check


@admin_session_check
def index(request):
    return render(request, 'admin/base.html', context={'name': 'Специализации'})


def admin_create_special(request):
    pass


def admin_edit_special(request):
    pass


def admin_delete_special(request):
    pass


urlpatterns = [
    path('', index),
    path('create/', admin_create_special),
    path('edit/', admin_edit_special),
    path('delete/', admin_delete_special),
]
