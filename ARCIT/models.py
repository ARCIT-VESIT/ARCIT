from django.core.files import File
from django.db import models

class DiagnosticDepartment(models.Model):
    name = models.CharField(max_length=100)
    DD_type = models.CharField(max_length=100)
    DD_license = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100, null=True)
    supervisor = models.CharField(max_length=100)
    referred_by = models.CharField(max_length=100)
    handled_by = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    report = models.FileField(upload_to='DiagnosticDepartment/report/',default='DiagnosticDepartment/report/xyz.txt')
    
    def __str__(self):
         return self.patient_name

class UserTypeModel(models.Model):
  usertype = models.CharField(max_length=6, 
            choices=(
                        ('1','Patient'),
                        ('2', 'Doctor'),
                    ), default='1')
