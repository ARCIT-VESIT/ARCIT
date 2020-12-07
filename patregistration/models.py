from django.db import models
from django.conf import settings


class Patients(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.BigIntegerField(unique=True)
    dob	= models.DateField()
    gender = models.CharField(max_length=20)
    weight = models.IntegerField()
    address = models.CharField(max_length=254)
    adharcardno = models.BigIntegerField(unique=True)
    blood_group = models.CharField(max_length=5, null=True)



# Create your models here.
