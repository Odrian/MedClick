from django.shortcuts import render, redirect
from django.urls import path, reverse

from admin.decorators import admin_session_check
from admin.models import Admin
from user.models import User


@admin_session_check
def admin_admin_index(request):
    admins = list(map(lambda x: x.user, Admin.objects.all()))
    return render(request, 'admin/admin.html', context={'path': 'Админы', 'admins': admins, 'length': len(admins)})


def admin_admin_index_post(request):
    lst = request.POST.getlist('_selected_action')
    action = request.POST.getlist('action')
    if not (isinstance(lst, list) and isinstance(action, list)):
        return redirect('..')
    if len(action) != 1:
        return redirect('..')

    admins = Admin.objects.filter(user__in=lst)

    action = action[0]
    if action == 'delete':
        for admin in admins:
            user = admin.user
            user.delete()
    elif action == 'freeze':
        for admin in admins:
            user = admin.user
            user.freeze = True
            user.save()
    elif action == 'unfreeze':
        for admin in admins:
            user = admin.user
            user.freeze = False
            user.save()
    return redirect('..')


@admin_session_check
def admin_admin_create(request):
    phone = request.GET.get('phone', '')
    name = request.GET.get('name', '')
    freeze = request.GET.get('freeze')
    return render(request, 'admin/admin_edit.html', context={'path': 'Админы', 'er': request.GET.get('er', '0'),
                                                            'phone': phone, 'name': name, 'freeze': freeze})


@admin_session_check
def admin_admin_create_post(request):
    phone = request.POST.get('phone')
    name = request.POST.get('name')
    freeze = request.POST.get('freeze')

    if not(isinstance(phone, str) and isinstance(name, str) and freeze in [None, 'on']):
        return redirect('..')

    freeze = bool(freeze)

    phone = phone.replace('+7', '8').replace(' ', '')
    if not (phone.isdecimal() and len(phone) == 11):
        return redirect('..?er=1&phone=' + phone + '&name=' + name + '&freeze=' + str(freeze))

    name = " ".join(map(lambda x: x.capitalize(), name.split()))
    if name == '':
        return redirect('..?er=2&phone=' + phone + '&name=' + name + '&freeze=' + str(freeze))

    if len(User.objects.filter(phone=phone)) != 0:
        return redirect('..?er=3&phone=' + phone + '&name=' + name + '&freeze=' + str(freeze))

    user = User(phone=phone, name=name, freeze=freeze, is_doctor=2)
    user.save()
    Admin(user=user).save()
    if request.POST.get('_save'):
        return redirect('../..')
    if request.POST.get('_addanother'):
        return redirect('..')
    if request.POST.get('_continue'):
        return redirect('../../' + str(user.pk))
    return redirect('../..')


@admin_session_check
def admin_admin_edit(request, user_id):
    admin = Admin.objects.filter(user=user_id)
    if len(admin) == 0:
        return redirect('..')
    admin = admin[0].user
    return render(request, 'admin/admin_edit.html', context={'path': 'Админы', 'er': request.GET.get('er', '0'), 'edit': 1,
                                                             'name': admin.name, 'phone': admin.phone, 'freeze': int(admin.freeze)})


@admin_session_check
def admin_admin_edit_post(request, user_id):
    admin = Admin.objects.filter(user=user_id)
    if len(admin) == 0:
        return redirect('../..')
    admin = admin[0].user

    phone = request.POST.get('phone')
    name = request.POST.get('name')
    freeze = request.POST.get('freeze')

    if not(isinstance(phone, str) and isinstance(name, str) and freeze in [None, 'on']):
        return redirect('..')

    freeze = bool(freeze)

    phone = phone.replace('+7', '8')
    if not (phone.isdecimal() and len(phone) == 11):
        return redirect('..?er=1&phone=' + phone + '&name=' + name + '&freeze=' + str(freeze))

    name = " ".join(map(lambda x: x.capitalize(), name.split()))
    if name == '':
        return redirect('..?er=2&phone=' + phone + '&name=' + name + '&freeze=' + str(freeze))

    if len(User.objects.filter(phone=phone)) != 0 and phone != admin.phone:
        return redirect('..?er=3&phone=' + phone + '&name=' + name + '&freeze=' + str(freeze))

    admin.name = name
    admin.phone = phone
    admin.freeze = freeze
    admin.save()

    if request.POST.get('_save'):
        return redirect('../..')
    if request.POST.get('_addanother'):
        return redirect('../../add')
    if request.POST.get('_continue'):
        return redirect('..')
    return redirect('../..')



@admin_session_check
def admin_admin_delete(request, user_id):
    admin = Admin.objects.filter(id=user_id)
    if len(admin):
        admin[0].user.delete()
    return redirect(reverse('admin.admin'))


urlpatterns = [
    path('', admin_admin_index),
    path('post/', admin_admin_index_post),
    path('add/', admin_admin_create),
    path('add/post/', admin_admin_create_post),
    path('<int:user_id>/', admin_admin_edit),
    path('<int:user_id>/post/', admin_admin_edit_post),
    path('<int:user_id>/delete/', admin_admin_delete),
]
