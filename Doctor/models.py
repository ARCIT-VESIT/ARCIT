from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Doctor(models.Model):
    id = models.BigAutoField(primary_key=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    created_on = models.DateTimeField(default=timezone.now, blank=False)
