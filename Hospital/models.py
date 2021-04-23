"""Hospital model"""
from django.db import models
from django.conf import settings

class Hospital(models.Model):
    '''Hospital model'''
    id = models.BigAutoField(primary_key=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    email = models.EmailField(max_length=254, unique=True)
    website = models.CharField(max_length=200, null=True, unique=True)
    registeration_number = models.IntegerField(unique=True)
    phone_number = models.BigIntegerField(unique=True)
    specialization = models.CharField(max_length=100,null=True)
