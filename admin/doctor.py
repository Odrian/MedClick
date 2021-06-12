from django.http import JsonResponse
from django.urls import path

from doctor.models import Doctor

from .decorators import admin_session_check


@admin_session_check
def admin_get_doctors(request):
    data = map(lambda x: x.user.get_data(), Doctor.objects.all())
    return JsonResponse({'info': 'all_ok', 'data': data})


def admin_create_doctor(request):
    pass


def admin_edit_doctor(request):
    pass


def admin_delete_doctor(request):
    pk = request.POST.get('id')
    if not isinstance(pk, int):
        return JsonResponse({'indo': 'unknown_type'})
    try:
        Doctor.objects.get(id=pk).user.delete()
    except Doctor.DoesNotExist:
        return JsonResponse({'info': 'this_id_not_exist'})
    return JsonResponse({'info': 'all_ok'})


urlpatterns = [
    path('get_all/', admin_get_doctors),
    path('create/', admin_create_doctor),
    path('edit/', admin_edit_doctor),
    path('delete/', admin_delete_doctor),
]
