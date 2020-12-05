from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    doctor_registeration_no = models.CharField(max_length = 30)
    email = models.EmailField(max_length=254)
    phone_number = models.IntegerField()
    experience = models.IntegerField()
    affiliation = models.CharField(max_length=100)
    accrediation = models.CharField(max_length=254)
    address = models.CharField(max_length=100)
    adharcardno = models.IntegerField()
    specialization = models.CharField(max_length=100)