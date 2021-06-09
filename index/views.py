from django.shortcuts import redirect, render


def index(request):  # Проверить сессию
    return render(request, 'index/index.html')
