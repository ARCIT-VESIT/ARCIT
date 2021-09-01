from django.db import models
from django.conf import settings
from django.utils import timezone

class Patient(models.Model):
    id = models.BigAutoField(primary_key=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.BigIntegerField(unique=True)
    dob	= models.DateField()
    gender = models.CharField(max_length=20)
    weight = models.IntegerField()
    address = models.CharField(max_length=254)
    pincode = models.IntegerField()
    state = models.CharField(max_length=254, null=True)
    adharcardno = models.BigIntegerField(unique=True)
    blood_group = models.CharField(max_length=5, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by', on_delete=models.CASCADE)

class PatientHistory(models.Model):	
    id = models.BigAutoField(primary_key=True)
    nonce = models.BigIntegerField()
    previous_hash = models.CharField(max_length=254)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    medical_status = models.CharField(max_length=50)
    symtomps = models.CharField(max_length=1000)
    disease	= models.CharField(max_length=200)
    affected_area = models.CharField(max_length=200)
    #report = models.FileField(upload_to='PatientHistory/report/', default = '', null=True)
    timespan = models.CharField(max_length=100)
    prescription = models.CharField(max_length=1000)
    course_duration = models.CharField(max_length=100)
    follow_up = models.CharField(max_length=100,null=True)
    referred_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='referred_from', on_delete=models.CASCADE)
    referred_to= models.CharField(max_length=100,null=True)
    created_on = models.DateTimeField(default=timezone.now, blank=False)

class Appointment(models.Model):
    id = models.BigAutoField(primary_key=True)
    patient_id = models.BigIntegerField()
    doctor_id = models.BigIntegerField()
    active_hour_id = models.BigIntegerField()
    date = models.DateField()
    token_number = models.BigIntegerField()
    is_treated = models.BooleanField(default=False)
    