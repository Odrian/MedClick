from django.urls import path
from .views import url_logout, url_phone, url_post_phone, url_phone_code, url_post_code#, url_register, url_post_register

urlpatterns = [
    path('logout/', url_logout, name='auth.logout'),

    path('phone/', url_phone, name='auth.phone'),
    path('post_phone/', url_post_phone, name='auth.post_phone'),

    path('code/', url_phone_code, name='auth.code'),
    path('post_code', url_post_code, name='auth.post_code'),

#    path('register/', url_register, name='auth.reg'),
#    path('post_register/', url_post_register, name='auth.post_reg'),
]
