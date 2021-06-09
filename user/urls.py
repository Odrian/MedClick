from django.urls import path
from .views import phone, post_phone, phone_code, post_code, register, post_register

urlpatterns = [
    path('phone/', phone, name='auth.phone'),
    path('post_phone/', post_phone, name='auth.post_phone'),

    path('code/', phone_code, name='auth.code'),
    path('post_code', post_code, name='auth.post_code'),

    path('register/', register, name='auth.reg'),
    path('post_register/', post_register, name='auth.post_reg'),
]
