import datetime
import os
from uuid import UUID

from django.utils.timezone import now
from django.urls import path
from django.http import HttpResponse
from rest_framework.decorators import api_view

from logic.auth import logic_phone, logic_code, logic_register

from .models import Session
from user.models import Register

from .decorators import convert_input


@api_view(['POST'])
@convert_input
def api_phone(request, post):
    resp = logic_phone(request.method, post.get('phone'))
    return HttpResponse(resp[0])


@api_view(['POST'])
@convert_input
def api_code(request, post):
    phone = post.get('phone')
    resp = logic_code(request.method, phone, post.get('code'))
    ans = {'info':resp[0], 'session_key': ''}
    if resp[0] == 'all_ok':
        if resp[1] == 'chat.main':
            ans['session_key'] = generate_uuid(phone)
        else:
            reg = Register.objects.filter(phone=phone)
            if len(reg) == 0:
                reg = Register(phone=phone)
                reg.save()
            else:
                reg[0].time = now()
    return HttpResponse(ans)


@api_view(['POST'])
@convert_input
def api_register(request, post):
    phone = post.get('phone')
    reg = Register.objects.filter(phone=phone)
    if len(reg) == 0:
        reg = None
    else:
        reg = reg[0]
        if now() > reg.time + datetime.timedelta(minutes=10):
            reg = None
    resp = logic_register(request, reg, phone)
    ans = {'info':resp[0], 'path':resp[1]}
    if resp[0] == 'all_ok':
        ans['session_key'] = generate_uuid(phone)
        reg.delete()
    return HttpResponse(ans)


def generate_uuid(phone):
    uuid = UUID(bytes=os.urandom(16), version=4)
    Session(key=uuid, phone=phone).save()
    return uuid


urlpatterns = [
    path('phone/', api_phone),
    path('code/', api_code),
    path('reg/', api_register),
]
