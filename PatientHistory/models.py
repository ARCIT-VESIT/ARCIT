from django.db import models

# Create your models here.
class PatientHistory(models.Model):	
    medical_status = models.CharField(max_length=50)
    symtomps = models.CharField(max_length=1000)
    disease	= models.CharField(max_length=200)
    affected_area = models.CharField(max_length=200)
    #report = models.FileField(upload_to=None, max_length=500, null=True)
    timespan = models.CharField(max_length=100)
    precription = models.CharField(max_length=1000)
    course_duration = models.CharField(max_length=100)
    follow_up = models.CharField(max_length=100,null=True)
    referred_from = models.CharField(max_length=100,null=True)
    referred_to= models.CharField(max_length=100,null=True)
