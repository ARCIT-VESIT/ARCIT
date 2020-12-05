from django.db import models

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