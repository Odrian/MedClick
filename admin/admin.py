from django.shortcuts import render, redirect
from django.urls import path, reverse

from admin.decorators import admin_session_check
from admin.models import Admin
from user.models import User


@admin_session_check
def index(request):
    admins = Admin.objects.all()

    freeze = request.GET.get('freeze')
    if freeze is not None:
        admins = admins.filter(user__freeze=freeze)

    serch = request.GET.get('q', '')
    if serch:
        admins_ = admins.filter(user__phone__icontains=serch)
        if len(admins_):
            admins = admins_
        else:
            admins = admins.filter(user__name__icontains=serch)

    admins = list(map(lambda x: x.user, admins))
    return render(request, 'admin/admin.html', context={'path': 'Админы', 'admins': admins, 'serch': serch,
                                                        'length': len(admins)})


def index_post(request):
    print(request.POST)
    if request.POST.get('filter') == '1':
        fr_1 = request.POST.get('filter_all')
        fr_2 = request.POST.get('filter_freeze')
        fr_3 = request.POST.get('filter_unfreeze')
        if fr_1:
            return redirect()
    else:
        lst = request.POST.getlist('_selected_action')
        action = request.POST.getlist('action')
        print(lst, action)
        if not (isinstance(lst, list) and isinstance(action, list)):
            print(1)
            return redirect('..')
        if len(action) != 1:
            print(2)
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
def admin_create_admin(request):
    phone = request.GET.get('phone', '')
    name = request.GET.get('name', '')
    freeze = request.GET.get('freeze')
    return render(request, 'admin/admin_edit.html', context={'path': 'Админы', 'er': request.GET.get('er', '0'),
                                                            'phone': phone, 'name': name, 'freeze': freeze})


@admin_session_check
def admin_create_admin_post(request):
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
def admin_delete_admin(request, user_id):
    admin = Admin.objects.filter(id=user_id)
    if len(admin):
        admin[0].user.delete()
    return redirect(reverse('admin.admin'))


urlpatterns = [
    path('', index),
    path('post/', index_post),
    path('add/', admin_create_admin),
    path('add/post/', admin_create_admin_post),
    path('<int:user_id>/', admin_edit_admin),
    path('<int:user_id>/post/', admin_edit_admin_post),
    path('<int:user_id>/delete/', admin_delete_admin),
]
