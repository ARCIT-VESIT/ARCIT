from django.core.files import File
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    is_diagnosticDepartment = models.BooleanField(default=False)