from django.shortcuts import redirect, render
from django.urls import reverse

from logic.chat import get_chat
from user.decorators import session_check


@session_check
def null_chat(request):
    return render(request, '', context={})


@session_check
def chat_view(request, chat_id):
    chat_list = get_chat(chat_id)
    if not chat_id in request.user.textchat_set:
        return redirect(reverse(''))
    return render(request, '', context={})
