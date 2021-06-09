import django
from django.db import models
from django.utils.crypto import salted_hmac


class UserManager(models.Manager):
    use_in_migrations = True


class User(models.Model):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, unique=True)
    birth_day = models.DateField()

    is_doctor = models.SmallIntegerField()
    last_login = models.DateTimeField(default=django.utils.timezone.now)
    date_joined = models.DateTimeField(default=django.utils.timezone.now)

    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def get_data(self):
        arr = {
            'id': self.pk,
            'name': self.full_name,
            'birth_day': self.birth_day}
        is_d = self.is_doctor
        if is_d == 0:
            arr.update(self.doctor.get_data())
        elif is_d == 1:
            arr.update(self.person.get_data())
        return arr

    def __str__(self):
        return self.phone

    def natural_key(self):
        return self.phone,

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def has_usable_password(self):
        return False

    def _legacy_get_session_auth_hash(self):
        key_salt = 'django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash'
        return salted_hmac(key_salt, self.phone, algorithm='sha1').hexdigest()

    def get_session_auth_hash(self):
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.phone, algorithm='sha256',).hexdigest()


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    objects = models.Manager()

    polis = models.CharField(max_length=16, null=True)

    def get_data(self):
        return {'polis': self.polis}



class UserCods(models.Model):
    phone = models.CharField(max_length=11, primary_key=True)
    code = models.IntegerField(null=True)
    code_time = models.DateTimeField(default=django.utils.timezone.now)

    objects = models.Manager()


class Register(models.Model):
    phone = models.CharField(max_length=11, primary_key=True)
    time = models.DateTimeField(default=django.utils.timezone.now)

    objects = models.Manager()
