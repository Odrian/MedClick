import datetime
import os
from uuid import UUID

from django.utils.timezone import now
from django.urls import path
from django.http import JsonResponse
from rest_framework.decorators import api_view

from logic.auth import logic_phone, logic_code, logic_register

from .models import Session
from user.models import Register


@api_view(['POST'])
def api_phone(request):
    resp = logic_phone(request.method, request.POST.get('phone'))
    return JsonResponse({'info':resp[0]})


@api_view(['POST'])
def api_code(request):
    phone = request.POST.get('phone')
    resp = logic_code(request.method, phone, request.POST.get('code'))
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
    return JsonResponse(ans)


@api_view(['POST'])
def api_register(request):
    phone = request.POST.get('phone')
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
    return JsonResponse(ans)


def generate_uuid(phone):
    uuid = UUID(bytes=os.urandom(16), version=4)
    Session(key=uuid, phone=phone).save()
    return uuid


urlpatterns = [
    path('phone/', api_phone),
    path('code/', api_code),
    path('reg/', api_register),
]
