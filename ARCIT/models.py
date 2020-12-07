from django.core.files import File
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    is_diagnosticDepartment = models.BooleanField(default=False)

class UserTypeModel(models.Model):
  usertype = models.CharField(max_length=6, 
            choices=(
                        (1,'Patient'),
                        (2, 'Doctor'),
                        (3, 'Hospital'),
                        (4, 'Diagnostic Department'),
                    ), default='1')
