from django.shortcuts import redirect, render


def index(request):  # Проверить сессию
    return render(request, 'index/index.html')


def create_doctors():
    from random import choice, randint
    from doctor.models import Doctor, Specialization
    from user.models import User
    sp = [(1, 'Акушер-гинеколог'), (2, 'Аллерголог'), (3, 'Дерматолог'), (4, 'Инфекционист'),
          (5, 'Кардиолог'), (6, 'Нарколог'), (7, 'Невропатолог'), (8, 'Педиатр'), (9, 'Психиатр'),
          (10, 'Стоматолог'), (11, 'Терапевт'), (12, 'Уролог'), (13, 'Физиотерапевт'), (14, 'Хирург')]
    names = ['Александр', 'Дмитрий', 'Максим', 'Сергей', 'Андрей', 'Алексей', 'Артём', 'Илья', 'Кирилл', 'Михаил',
             'Никита', 'Матвей', 'Роман', 'Егор', 'Арсений', 'Иван', 'Денис', 'Евгений', 'Даниил', 'Тимофей',
             'Владислав', 'Игорь', 'Владимир', 'Павел', 'Руслан', 'Марк', 'Константин', 'Тимур', 'Олег', 'Ярослав']
    sunames = ['Смирнов', 'Иванов', 'Кузнецов', 'Соколов', 'Попов', 'Лебедев', 'Козлов', 'Новиков', 'Морозов',
               'Петров', 'Волков', 'Соловьёв', 'Васильев', 'Зайцев', 'Павлов', 'Семёнов', 'Голубев', 'Виноградов',
               'Богданов', 'Воробьёв', 'Фёдоров', 'Михайлов', 'Беляев', 'Тарасов', 'Белов', 'Комаров', 'Орлов',
               'Киселёв', 'Макаров', 'Андреев']
    phone = 89960001000
    for i in sp:
        Specialization(id=i[0], name=i[1]).save()
    ln = len(sp)
    for i in range(1, ln + 1):
        for j in range(randint(3, 7)):
            name = choice(names)
            suname = choice(sunames)
            full_name = name + ' ' + suname
            user = User(name=full_name, phone=phone, is_doctor=True)
            user.save()
            doctor = Doctor(user_id=user.pk, cost=(randint(1, 10) * 50), experience=(str(randint(1, 7)) + ' лет'),
                   service_types='Любой', work_time='Всегда', educations='Высшее', extra_field='')
            doctor.save()
            doctor.specifications.add(i)
            phone += 1

#create_doctors()
