from django.shortcuts import render, redirect
from django.urls import reverse

from doctor.models import Doctor
from logic.auth import logic_phone, logic_code, logic_register
from user.models import Register


def url_logout(request):
    request.session.clear()


def url_phone(request):
    return render(request, 'user/phone.html')


def url_phone_code(request):
    if not request.session.get('phone'):  # Проверка прохождение предыдущего этапа
        return redirect(reverse('auth.phone'))

    return render(request, 'user/code.html')


'''def url_register(request):
    if len(Register.objects.filter(phone=request.session.get('phone'))) == 0:  # Проверка подтверждённого телефона
        return redirect(reverse('auth.phone'))

    return render(request, 'user/register.html')'''



def url_post_phone(request):
    phone = request.POST.get('phone')
    if not isinstance(phone, str):
        resp = ['unread_phone', 'auth.phone']
    else:
        if len(phone) > 15:
            return ['too_long_phone', 'auth.phone']
        phone = '+7' + phone
        resp = ['unknown_user', 'auth.phone']
        if len(Doctor.objects.filter(phone=phone)) != 0:
            resp = logic_phone(request.method, phone)
            if resp[0] == 'all_ok':
                request.session['phone'] = phone
    return redirect(reverse(resp[1]))


def url_post_code(request):
    phone = request.session.get('phone')
    code = request.POST.get('code')
    if not (isinstance(phone, str) and isinstance(code, int)):
        resp = ['unread_phone', 'auth.phone']
    else:
        resp = logic_code(request.method, phone, code)
        if resp[1] == 'chat.main':
            request.session['login'] = True
    return redirect(reverse(resp[1]))


'''def url_post_register(request):
    phone = request.session.get('phone')
    if not isinstance(phone, str):
        resp = ['unread_phone', 'auth.phone']
    esle:
        resp = logic_register(request, len(Register.objects.filter(phone=phone)) != 0, tele_phone)
        if resp[1] == 'all_ok':
            Register.objects.filter(phone=tele_phone).delete()
            request.session['login'] = True
    return redirect(reverse(resp[1]))'''
