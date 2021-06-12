import datetime
import json
import urllib
from random import randint

from django.utils.timezone import now

from MedClick.settings import GOOGLE_RECAPTCHA_SECRET_KEY
from user.models import User, UserCods, Person


def logic_phone(method, phone):
    if method != 'POST':
        return ['incorrect_method', 'auth.phone']
    if not phone:
        return ['null_phone', 'auth.phone']
    if not len(phone) <= 14:
        return ['incorrect_phone', 'auth.phone']

    user_cods = UserCods.objects.filter(phone=phone)
    if len(user_cods) == 1:
        user_cod = user_cods[0]
    else:
        user_cod = UserCods(phone=phone)
        user_cod.save()

    generare_code(user_cod)
    send_sms(user_cod)
    return ['all_ok', 'auth.code']


def logic_code(method, phone, code):
    if method != 'POST':
        return ['incorrect_method', 'auth.phone']

    if not phone:
        return ['null_phone', 'auth.phone']

    user_cods = UserCods.objects.filter(phone=phone)
    if len(user_cods) != 1:
        return ['null_phone', 'auth.phone']

    if not code:
        return ['null_code', 'auth.phone']

    user_cod = user_cods[0]
    if now() > user_cod.code_time + datetime.timedelta(minutes=10):
        return ['code_time_eror', 'auth.phone']
    if code != str(user_cod.code):
        return ['incorrect_code', 'auth.phone']

    user_cod.delete()
    user = User.objects.filter(phone=phone)
    if len(user) == 0:
        return ['all_ok', 'auth.reg']
    else:
        user = user[0]
        user.last_login = now()
        user.save(update_fields=['last_login'])
        return ['all_ok', 'chat.main']


def logic_register(request, registrate, phone):
    if request.method != 'POST':
        return ['incorrect_method', 'auth.phone']
    if not registrate:
        return ['dont_confirm_phone', 'auth.phone']

    if not phone:
        return ['null_phone', 'auth.phone']

    name = request.POST.get('name')
    name = " ".join(name.split())
    if len(name) > 50:
        return ['too_long_name', 'auth.reg']

    birth_day = request.POST.get('birth_day')
    if not birth_day:
        return ['null_birth_day', 'auth.reg']
    birth_day = list(map(int, birth_day.split('-')))
    try:
        birth_day = datetime.date(year=birth_day[0], month=birth_day[1], day=birth_day[2])
    except ValueError:
        return ['incorrect_date', 'auth.reg']
    if not datetime.date(day=1, month=1, year=1800) < birth_day < now().date():
        return ['false_date', 'auth.reg']
    birth_day = datetime.datetime.combine(birth_day, datetime.time(0, 0, 0))

    polis = request.POST.get('polis')
    if polis:
        if len(polis) != 16:
            return ['incorrect_polis', 'auth.reg']

    user = User(phone=phone, name=name, date_joined=now().date(), is_doctor=0)
    user.save()
    person = Person(user=user, birth_day=birth_day, polis=polis)
    person.save()
    return ['all_ok', 'chat.main']




def generare_code(user_cods):
    code = ''.join([str(randint(0, 9)) for i in range(4)])
    print(code)
    user_cods.code = code
    user_cods.code_time = now()
    user_cods.save()


def send_sms(user):
    phone = user.phone
    code = user.code
    if phone and code:
        pass


def check_recapcha(recaptcha_response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response}
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result['success']
