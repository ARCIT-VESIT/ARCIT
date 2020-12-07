from django.db import models
from django.conf import settings

class DiagnosticDepartment(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    DD_type = models.CharField(max_length=100)
    DD_license = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    website = models.CharField(max_length=100)
    registeration_number = models.IntegerField()
    phone_number = models.IntegerField()
    specialization = models.CharField(max_length=100)

class DiagnosticDepartmentReport(models.Model):
    name = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=100)
    referred_by = models.CharField(max_length=100)
    handled_by = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    report = models.FileField(upload_to='DiagnosticDepartment/report/')
    
    def __str__(self):
         return self.patient_name