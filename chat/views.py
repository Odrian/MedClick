from django.shortcuts import redirect, render
from django.urls import reverse, path

from chat.models import Checker
from logic.chat import get_chat
from user.decorators import session_check
from user.models import User


@session_check
def null_chat(request):
    return render(request, 'chat/chat.html', context={})


@session_check
def chat_view(request, chat_id):
    user = User.objects.get(phone=request.session.get('phone'))
    if len(Checker.objects.filter(user=user, chat=chat_id)) == 0:
        return redirect(reverse('chat.main'))
    return render(request, 'chat/chat.html', context={'chat': get_chat(chat_id)})


def chat_help(request):
    return chat_view(request, 'adrian_id')


urlpatterns = [
    path('', null_chat, name='chat.main'),
    path('<int:chat_id>/', chat_view),
    path('help/', chat_help)
]
