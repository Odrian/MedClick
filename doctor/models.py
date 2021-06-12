from django.db import models

from user.models import User


class Specialization(models.Model):
    name = models.CharField(max_length=64, unique=True)
    objects = models.Manager()

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    objects = models.Manager()

    cost = models.IntegerField(null=True)
    experience = models.TextField(null=True)
    service_types = models.TextField(null=True)
    work_time = models.TextField(null=True)
    educations = models.TextField(null=True)
    specifications = models.ManyToManyField(Specialization)
    extra_field = models.TextField(null=True)

    def get_data(self):
        return {
            'cost': self.cost,
            'experience': self.experience,
            'service_types': self.service_types,
            'work_time': self.work_time,
            'educations': self.educations,
            'specifications': list(map(lambda x: x.name, self.specifications.all())),
            'extra_field': self.extra_field}
