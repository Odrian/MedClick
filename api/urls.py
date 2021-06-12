from django.urls import path, include


urlpatterns = [
    path('admin/', include('api.admin')),
    path('auth/', include('api.auth')),
    path('chat/', include('api.chat')),
    path('profile/', include('api.profile'))
]
