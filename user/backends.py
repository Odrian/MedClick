"""class ModelBackend:
    pass
"""
from .models import User

class ModelBackend:
    def authenticate(self, request, phone):
        print(1)
        if phone is None:
            return
        user = User.objects.filter(phone=phone)
        print(2)
        if len(user) == 0:
            return
        print(3)
        return user[0]

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user
