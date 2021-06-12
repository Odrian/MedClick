from django.http import JsonResponse
from django.urls import path

from doctor.models import Specialization

from .decorators import admin_session_check


@admin_session_check
def admin_get_specials(request):
    data = map(lambda x: [x.pk, x.name], Specialization.objects.all())
    return JsonResponse({'info': 'all_ok', 'data': data})


@admin_session_check
def admin_create_special(request):
    name = request.POST.get('name', '')
    if not isinstance(name, str):
        return JsonResponse({'indo': 'unknown_type'})
    if len(Specialization.objects.filter(name=name)) != 0:
        return JsonResponse({'info': 'this_name_already_exist'})
    spec = Specialization(name=name)
    spec.save()
    return JsonResponse({'info': 'all_ok', 'id': spec.id})


@admin_session_check
def admin_edit_special(request):
    pk = request.POST.get('id')
    name = request.POST.get('id')
    if not (isinstance(name, str) and isinstance(pk, int)):
        return JsonResponse({'indo': 'unknown_type'})
    try:
        spec = Specialization.objects.get(id=pk)
    except Specialization.DoesNotExist:
        return JsonResponse({'info': 'this_name_already_exist'})
    spec.name = name
    spec.save()
    return JsonResponse({'info': 'all_ok'})


@admin_session_check
def admin_delete_special(request):
    pk = request.POST.get('id')
    if not isinstance(pk, int):
        return JsonResponse({'indo': 'unknown_type'})
    try:
        Specialization.objects.get(id=pk).delete()
    except Specialization.DoesNotExist:
        return JsonResponse({'info': 'this_id_not_exist'})
    return JsonResponse({'info': 'all_ok'})


urlpatterns = [
    path('get_all/', admin_get_specials),
    path('create/', admin_create_special),
    path('edit/', admin_edit_special),
    path('delete/', admin_delete_special),
]
