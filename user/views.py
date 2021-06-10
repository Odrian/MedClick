from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.timezone import now

from doctor.models import Doctor
from logic.auth import logic_phone, logic_code, logic_register
from user.models import Register


def phone(request):
    return render(request, 'user/phone.html')


def phone_code(request):
    if not request.session.get('phone'):  # Проверка прохождение предыдущего этапа
        return redirect(reverse('auth.phone'))

    return render(request, 'user/code.html')


def register(request):
    if len(Register.objects.filter(phone=request.session.get('phone'))) == 0:  # Проверка подтверждённого телефона
        return redirect(reverse('auth.phone'))

    return render(request, 'user/register.html')



def post_phone(request):
    tele_phone = request.POST.get('phone')
    if not isinstance(tele_phone, str):
        resp = ['unread_phone', 'auth.phone']
    else:
        tele_phone = '8' + tele_phone
        resp = ['unknown_user', 'auth.phone']
        if len(Doctor.objects.filter(phone=tele_phone)) != 0:
            resp = logic_phone(request.method, tele_phone)
            if resp[0] == 'all_ok':
                request.session['phone'] = tele_phone
    return redirect(reverse(resp[1]))


def post_code(request):
    tele_phone = request.session.get('phone')
    resp = logic_code(request.method, tele_phone, request.POST.get('code'))
    if resp[1] == 'chat.main':
        request.session['login'] = True
    return redirect(reverse(resp[1]))


def post_register(request):
    tele_phone = request.session.get('phone')
    resp = logic_register(request, len(Register.objects.filter(phone=tele_phone)) != 0, tele_phone)
    if resp[1] == 'all_ok':
        Register.objects.filter(phone=tele_phone).delete()
        request.session['login'] = True
    return redirect(reverse(resp[1]))
