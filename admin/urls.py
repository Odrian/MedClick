from django.urls import path, include

urlpatterns = [
    path('doctor/', include('admin.doctor')),
    path('special/', include('admin.special')),
    path('stat/', include('admin.stat')),
]
