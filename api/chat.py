from django.http import JsonResponse, HttpResponse
from django.urls import path
from rest_framework.decorators import api_view

from user.models import User
from .decorators import session_check
from logic.chat import get_chat, add_message, make_chat, get_file, get_chat_list, set_chat_checked


@api_view(['POST'])
@session_check
def api_chat_list(request, phone):
    return JsonResponse({'info': 'all_ok', 'data': get_chat_list(phone)})


@api_view(['POST'])
@session_check
def api_check(request, phone):
    chats = User.objects.get(phone=phone).chatlist_set.filter(check=False)
    data = list(map(lambda x: x.chat.pk, chats))
    return {'info': 'all_ok', 'data': data}


@api_view(['POST'])
@session_check
def api_create_chat(request, phone):
    phones = request.POST.getlist('phones')
    if not isinstance(phones, list):
        return JsonResponse({'info':'unread_phones'})
    phones.append(phone)
    chat_id = make_chat(phones)
    set_chat_checked(chat_id, phone, True)
    return JsonResponse({'info': 'all_ok', 'chat_id': chat_id})




@api_view(['POST'])
@session_check
def api_get_chat(request, chat_id, phone):
    if check_chat(chat_id, phone):
        return JsonResponse({'info':'unknown_chat'})
    chat = get_chat(chat_id)
    set_chat_checked(chat_id, phone, True)
    return JsonResponse({'info':'all_ok', 'chat':chat})


@api_view(['POST'])
@session_check
def api_send_message(request, chat_id, phone):
    if check_chat(chat_id, phone):
        return JsonResponse({'info':'unknown_chat'})
    text = request.POST.get('message', '')
    if not isinstance(text, str):
        return JsonResponse({'info': 'unknown_message_type'})
    file = request.FILES.get('file')
    file_type = request.POST.get('file_type')
    if file_type not in ['img', 'audio']:
        return JsonResponse({'info': 'inknown_file_type'})
    if text == '' and (file or file_type):
        return JsonResponse({'info':'null_text_and_file'})
    add_message(chat_id, phone, text, file, file_type)
    return JsonResponse({'info':'all_ok'})


@api_view(['POST'])
@session_check
def api_get_file(request, chat_id, file_id, phone):
    if check_chat(chat_id, phone):
        return JsonResponse({'info':'unknown_chat'})
    file = get_file(chat_id, file_id)
    if file == 'error':
        return JsonResponse({'info':'unknown_file'})
    response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'inline; filename=' + str(file_id)
    return response


def check_chat(chat_id, phone):
    chats = User.objects.get(phone=phone).textchat_set.all().filter(pk=chat_id)
    return not bool(chats)


urlpatterns = [
    path('chat_list/', api_chat_list),
    path('check/', api_check),
    path('create_chat/', api_create_chat),

    path('<int:chat_id>/', api_get_chat),
    path('<int:chat_id>/send_message/', api_send_message),
    path('<int:chat_id>/<int:file_id>/', api_get_file),
]
