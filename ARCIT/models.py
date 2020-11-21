from django.db import models

class Patients(models.Model):
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

class PatientHistory(models.Model):	
    medical_status = models.IntegerField()
    symtomps = models.CharField(max_length=1000)
    disease	= models.CharField(max_length=200)
    affected_area = models.CharField(max_length=200)
    report = models.FileField(upload_to=None, max_length=500, null=True)
    timespan = models.CharField(max_length=100)
    precription = models.CharField(max_length=1000)
    course_duration = models.CharField(max_length=100)
    follow_up = models.CharField(max_length=100,null=True)
    referred_from = models.CharField(max_length=100,null=True)
    referred_to= models.CharField(max_length=100,null=True)

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=True)
    doctor_registeration_no = models.CharField(max_length = 30,unique=True)
    email = models.EmailField(max_length=254,unique=True)
    phone_number = models.BigIntegerField(unique=True)
    experience = models.IntegerField(null=True)
    affiliation = models.CharField(max_length=100, null=True)
    accrediation = models.CharField(max_length=254)
    address = models.CharField(max_length=100)
    adharcardno = models.BigIntegerField(unique=True)
    specialization = models.CharField(max_length=100,null=True)

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    email = models.EmailField(max_length=254, unique=True)
    website = models.CharField(max_length=200, null=True)
    registeration_number = models.IntegerField()
    phone_number = models.BigIntegerField(unique=True)
    specialization = models.CharField(max_length=100,null=True)

class DiagnosticDepartment(models.Model):
    name = models.CharField(max_length=100)
    DD_type = models.CharField(max_length=100)
    DD_license = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100, null=True)
    supervisor = models.CharField(max_length=100)
    referred_by = models.CharField(max_length=100)
    handled_by = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)