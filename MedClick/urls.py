from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from index.views import index

from django.contrib import admin

urlpatterns = [
    path('', index),
    path('auth/', include('user.urls')),
    path('chat/', include('chat.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
#    path('admin_new/', include('admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
