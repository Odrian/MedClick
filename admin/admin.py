from django.shortcuts import render, redirect
from django.urls import path, reverse

from admin.decorators import admin_session_check
from admin.models import Admin
from user.models import User


@admin_session_check
def index(request):
    admins = Admin.objects.all()

    is_freeze = request.GET.get('is_freeze')
    if is_freeze is not None:
        admins = admins.filter(user__freeze=is_freeze)

    serch = request.GET.get('q', '')
    if serch:
        admins_ = admins.filter(user__phone__icontains=serch)
        if len(admins_):
            admins = admins_
        else:
            admins = admins.filter(user__name__icontains=serch)

    admins = list(map(lambda x: x.user, admins))
    return render(request, 'admin/admin.html', context={'path': 'Админы', 'admins': admins, 'serch': serch})


@admin_session_check
def admin_create_admin(request):
    phone = request.GET.get('phone', '')
    FIO = request.GET.get('FIO', '')
    freeze = request.GET.get('freeze')
    return render(request, 'admin/admin_edit.html', context={'path': 'Админы', 'er': request.GET.get('er', '0'),
                                                            'phone': phone, 'FIO': FIO, 'freeze': freeze})


@admin_session_check
def admin_create_admin_post(request):
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
def admin_edit_admin(request, user_id):
    admin = Admin.objects.filter(user=user_id)
    if len(admin) == 0:
        return redirect('..')
    admin = admin[0].user
    print(admin.freeze)
    return render(request, 'admin/admin_edit.html', context={'path': 'Админы', 'er': request.GET.get('er', '0'), 'edit': 1,
                                                             'name': admin.name, 'phone': admin.phone, 'freeze': int(admin.freeze)})


@admin_session_check
def admin_edit_admin_post(request, user_id):
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
        return redirect('..?er=3&phone=' + phone + '&name=' + name + '&freeze=' + str(freeze))

    name = " ".join(map(lambda x: x.capitalize(), name.split()))
    if name == '':
        return redirect('..?er=2&phone=' + phone + '&name=' + name + '&freeze=' + str(freeze))

    if len(User.objects.filter(phone=phone)) != 0:
        return redirect('..?er=3&phone=' + phone + '&name=' + name + '&freeze=' + str(freeze))

    admin.name = name
    admin.phone = phone
    admin.freeze = freeze
    admin.save()

    if request.POST.get('_save'):
        return redirect('../..')
    if request.POST.get('_addanother'):
        return redirect('..')
    if request.POST.get('_continue'):
        return redirect('../../' + str(user.pk))
    return redirect('../..')



@admin_session_check
def admin_delete_admin(request, user_id):
    admin = Admin.objects.filter(id=user_id)
    if len(admin):
        admin[0].user.delete()
    return redirect(reverse('admin.admin'))


urlpatterns = [
    path('', index),
    path('add/', admin_create_admin),
    path('add/post/', admin_create_admin_post),
    path('<int:user_id>/', admin_edit_admin),
    path('<int:user_id>/post/', admin_edit_admin_post),
    path('<int:user_id>/delete/', admin_delete_admin),
]
