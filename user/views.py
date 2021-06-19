from django.shortcuts import render, redirect
from django.urls import reverse, path

from logic.auth import logic_phone, logic_code#, logic_register
#from user.models import Register
from user.models import User


def url_logout(request):
    request.session['phone'] = ''
    return redirect(reverse('auth.phone'))


def url_phone(request):
    return render(request, 'user/phone.html')

def url_phone_code(request):
    if not request.session.get('phone_login'):
        return redirect(reverse('auth.phone'))
    return render(request, 'user/code.html')

'''def url_register(request):
    if len(Register.objects.filter(phone=request.session.get('phone'))) == 0:
        return redirect(reverse('auth.phone'))
    return render(request, 'user/register.html')'''


def url_post_phone(request):
    phone = request.POST.get('phone')
    if not isinstance(phone, str):
        return redirect(reverse('auth.phone'))
    if len(phone) != 10:
        return redirect(reverse('auth.phone'))
    phone = '8' + phone
    if len(User.objects.filter(phone=phone)) == 0:
        return redirect(reverse('auth.phone'))
    resp = logic_phone(request.method, phone)
    if resp[0] == 'all_ok':
        request.session['phone_login'] = phone
    return redirect(reverse(resp[1]))


def url_post_code(request):
    phone = request.session.get('phone_login')
    code = request.POST.get('code')
    if not (isinstance(phone, str) and isinstance(code, str)):
        return redirect(reverse('auth.phone'))
    resp = logic_code(request.method, phone, code)
    if resp[1] == 'chat.main':
        del request.session['phone_login']
        request.session['phone'] = phone
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


urlpatterns = [
    path('logout/', url_logout, name='auth.logout'),

    path('phone/', url_phone, name='auth.phone'),
    path('post_phone/', url_post_phone, name='auth.post_phone'),

    path('code/', url_phone_code, name='auth.code'),
    path('post_code', url_post_code, name='auth.post_code'),

#    path('register/', url_register, name='auth.reg'),
#    path('post_register/', url_post_register, name='auth.post_reg'),
]
