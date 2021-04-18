"""Hospital model"""
from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Hospital(models.Model):
    '''Hospital model'''
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    email = models.EmailField(max_length=254, unique=True)
    website = models.CharField(max_length=200, null=True)
    registeration_number = models.IntegerField()
    phone_number = models.BigIntegerField(unique=True)
    specialization = models.CharField(max_length=100,null=True)
    created_on = models.DateTimeField(default=timezone.now, blank=False)
