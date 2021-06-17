from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from index.views import index


urlpatterns = [
    path('', index),
    path('auth/', include('user.urls')),
    path('chat/', include('chat.views')),
    path('api/', include('api.urls')),
    path('admin/', include('admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
