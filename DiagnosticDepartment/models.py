from django.db import models
from django.conf import settings
from django.utils import timezone

class DiagnosticDepartment(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    id = models.BigAutoField(primary_key=True)
    patient_history_id = models.BigIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='dd_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    supervisor = models.CharField(max_length=100)
    referred_by = models.CharField(max_length=100)
    report = models.FileField()
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='handled_by', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now, blank=False)
