from django.db import models
from django.conf import settings
from django.db.models.fields import json
from django.db.models.fields.json import JSONField

class ActiveHour(models.Model):
    id = models.BigAutoField(primary_key=True)
    doctor_id=models.IntegerField()
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    departure_time = models.TimeField(auto_now=False, auto_now_add=False)
    for_hospital = models.BooleanField(null=True, default=False)

class Doctor(models.Model):
    id = models.BigAutoField(primary_key=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    doctor_registeration_no = models.CharField(max_length = 30, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.BigIntegerField(unique=True)
    experience = models.IntegerField()
    affiliation = models.CharField(max_length=100)
    accreditation = models.CharField(max_length=254)
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    adharcardno = models.IntegerField(unique=True)
    specialization = models.CharField(max_length=100)
    active_hours = JSONField(default=list)

    def set_active_hours(self, x):
        self.active_hours = json.dumps(x)

    def get_active_hours(self):
        return json.loads(self.active_hours)
