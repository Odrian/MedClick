class ModelBackend:
    pass

'''
from django.contrib.auth import get_user_model

User = get_user_model()

class ModelBackend:
    def authenticate(self, request, phone):
        if phone is None:
            return
        user = User.objects.filter(phone=phone)
        if len(user) == 0:
            return
        return user[0]

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user
'''
