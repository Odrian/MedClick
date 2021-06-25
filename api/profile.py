import datetime

from django.http import JsonResponse
from django.urls import path
from django.utils.timezone import now
from rest_framework.decorators import api_view

from user.models import User
from doctor.models import Doctor, Specialization

from .decorators import session_check


@api_view(['POST'])
@session_check
def api_all_jobs(request, phone):
    data = list(map(lambda x: [x.pk, x.name], Specialization.objects.all()))
    data2 = {}
    for i in data:
        data2[i[0]] = i[1]
    return JsonResponse({'info': 'all_ok', 'data': data2})


@api_view(['POST'])
@session_check
def api_all_doctors(request, phone):
    data = Doctor.objects.all()

    job = request.POST.get('job')
    if job:
        jobs = Specialization.objects.filter(name=job)
        if not jobs:
            data = data.filter(specifications__in=[int(jobs[0])])

    name = request.POST.get('name')
    if name:
        name = ' '.join(name.split()).title()
        data = data.filter(user__name__contains=name)

    data = list(map(lambda x: x.user.get_data(), data))
    return JsonResponse({'info': 'all_ok', 'data': data})


@api_view(['POST'])
@session_check
def api_get_doctor_info(request, phone):
    data = Doctor.objects.filter(user_id=request.POST.get('dortor_id'))
    if len(data) == 0:
        return JsonResponse({'info': 'unknown_doctor'})
    data = data[0].user.get_data()
    return JsonResponse({'info': 'all_ok', 'data': data})


@api_view(['POST'])
@session_check
def api_get_self(request, phone):
    data = User.objects.get(phone=phone).get_data()
    return JsonResponse({'info': 'all_ok', 'data': data})



@api_view(['POST'])
@session_check
def api_edit_self(request, phone):
    user = User.objects.get(phone=phone)

    name = request.POST.get('name')
    if isinstance(name, str):
        name = " ".join(name.split())
        if len(name) <= 50:
            user.name = name

    birth_day = request.POST.get('birth_day')
    if isinstance(birth_day, str):
        birth_day = list(map(int, birth_day.split('-')))
        try:
            birth_day = datetime.date(year=birth_day[0], month=birth_day[1], day=birth_day[2])
        except ValueError:
            return ['incorrect_date', 'auth.reg']
        if not datetime.date(day=1, month=1, year=1800) < birth_day < now().date():
            return ['false_date', 'auth.reg']
        birth_day = datetime.datetime.combine(birth_day, datetime.time(0, 0, 0))
        user.birth_day = birth_day
    user.save()

    if user.is_doctor:
        doctor = user.doctor

        cost = request.POST.get('cost')
        if isinstance(cost, int):
            if 0 <= cost <= 10000:
                doctor.cost = cost

        experience = request.POST.get('experience')
        if isinstance(experience, str):
            doctor.experience = experience

        service_types = request.POST.get('service_types')
        if isinstance(service_types, str):
            doctor.service_types = service_types

        work_time = request.POST.get('work_time')
        if isinstance(work_time, str):
            doctor.work_time = work_time

        educations = request.POST.get('educations')
        if isinstance(educations, str):
            doctor.educations = educations

        specifications = request.POST.get('specifications')
        if isinstance(specifications, list):
            doctor.specifications.clear()
            for pk in specifications:
                if isinstance(pk, int):
                    if len(Specialization.objects.filter(pk=pk)) == 1:
                        doctor.specifications.add(pk)

        extra_field = request.POST.get('extra_field')
        if isinstance(extra_field, str):
            doctor.experience = extra_field

        doctor.save()
    else:
        polis = request.POST.get('polis')
        if isinstance(polis, str):
            if len(polis) == 16:
                person = user.person
                person.polis = polis
                person.save()

    return JsonResponse({'info': 'all_ok'})

urlpatterns = [
    path('get_jobs/', api_all_jobs),
    path('get_doctors/', api_all_doctors),
    path('<int:doctor_id>/', api_get_doctor_info),
    path('self/', api_get_self),
    path('self/edit/', api_edit_self),
]
