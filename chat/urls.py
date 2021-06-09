from django.urls import path

from .views import chat_view, null_chat

urlpatterns = [
    path('', null_chat, name='chat.main'),
    path('<int:chat_id>/', chat_view),
]
