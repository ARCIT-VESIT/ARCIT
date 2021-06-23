from django.db import models
from django.conf import settings

class Doctor(models.Model):
    id = models.BigAutoField(primary_key=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    doctor_registeration_no = models.CharField(max_length = 30, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.IntegerField(unique=True)
    experience = models.IntegerField()
    affiliation = models.CharField(max_length=100)
    accreditation = models.CharField(max_length=254)
    address = models.CharField(max_length=100)
    adharcardno = models.IntegerField(unique=True)
    specialization = models.CharField(max_length=100)
