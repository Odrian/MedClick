import json
import os

from django.utils.timezone import now

from MedClick.settings import MEDIA_ROOT
from chat.models import Chat, Checker
from user.models import User


def set_chat_checked(chat_id, phone, checked):
    User.objects.get(phone=phone).checker_set.get(chat=chat_id).check = checked


def get_chat_list(phone):
    chat_list = User.objects.get(phone=phone).textchat_set.all()
    return list(map(lambda x: [x.id, x.chatlist.check], chat_list))


def get_chat(chat_id):
    path = os.path.join(MEDIA_ROOT, 'chats', str(chat_id), 'data.json')
    with open(path, encoding='utf-8') as file:
        return json.load(file)


def add_message(chat_id, phone, text, file, file_type):
    chat = get_chat(str(chat_id))
    user = User.objects.get(phone=phone)
    pk = user.pk
    name = user.name
    time = now()
    time = time.strftime('%d-%m-%Y %H:%M:%S')

    message = {'id': pk, 'name':name, 'phone':phone, 'date':time, 'text':text}
    if file and file_type:
        fc = chat['file_count']
        chat['file_count'] += 1
        message['file'] = {'id': fc, 'type': file_type}
        file_save(chat_id, fc, file)
    chat['chat'].append(message)
    save_chat(chat_id, chat)

    for checker in Chat.objects.get(id=chat_id).checker_set.all():
        checker.check = False


def save_chat(chat_id, chat):
    path = os.path.join(MEDIA_ROOT, 'chats', str(chat_id))
    os.makedirs(path, exist_ok=True)
    path = os.path.join(path, 'data.json')
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(chat, file, ensure_ascii=False)


def make_chat(phones):
    chat = Chat()
    chat.save()
    ln = 0
    for phone in phones:
        user = User.objects.filter(phone=phone)
        if len(user) != 0:
            ln += 1
            user = user[0]
            Checker(user=user, chat=chat).save()
    pk = chat.pk
    save_chat(pk, {"members": ln, "file_count": 0, "chat": []})
    return pk


def add_user_to_chat(phone, chat_id):
    user = User.objects.get(phone=phone)
    chat = Chat.objects.get(id=chat_id)
    Checker(user=user, chat=chat).save()


def file_save(chat_id, file_id, f):
    dir_id = chat_id // 100

    path = os.path.join(MEDIA_ROOT, 'chats', str(chat_id), 'files', str(dir_id))
    os.makedirs(path, exist_ok=True)
    path = os.path.join(path, str(file_id))

    with open(path, 'wb') as file:
        for chunk in f.chunks():
            file.write(chunk)


def get_file(chat_id, file_id):
    dir_id = file_id // 100
    path = os.path.join(MEDIA_ROOT, 'chats', str(chat_id), 'files', str(dir_id), str(file_id))
    if not os.path.exists(path):
        return 'error'
    return open(path, 'rb')
