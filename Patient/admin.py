from django.contrib import admin
from .models import Patients, PatientHistory

admin.site.register(Patients)
admin.site.register(PatientHistory)

# Register your models here.
