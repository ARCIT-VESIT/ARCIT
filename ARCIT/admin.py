from django.contrib import admin
from .models import Patients, PatientHistory, Doctor, Hospital, DiagnosticDepartment

admin.site.register(Patients)
admin.site.register(PatientHistory)
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(DiagnosticDepartment)