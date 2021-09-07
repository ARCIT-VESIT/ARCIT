from django.contrib import admin
from .models import Patient, PatientHistory, Appointment

admin.site.register(Patient)
admin.site.register(PatientHistory)
admin.site.register(Appointment)
