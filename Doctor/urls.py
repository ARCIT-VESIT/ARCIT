"""Url for doctor"""
from django.urls import path
from django.conf.urls import url
from Doctor import views as DoctorView

urlpatterns = [
    url(r'^d/profile/$',
        DoctorView.ViewDoctorProfile.as_view(template_name='Doctor/profile.html'),
        name='doctorprofile'),
    url(r'^p/addDiagnosis/$',
        DoctorView.AddPatientDataView.as_view(template_name='Doctor/addPatientHistory.html'),
        name='PatientHistory'),
    path('d/patient_treated', DoctorView.dashboard_data, name='patient_treated'),
    path('d/dashboard/', DoctorView.dashboard, name='doctor_dashboard'),
    path('d/dashboard_data', DoctorView.dashboard_data, name='doctor_dashboard_data'),
    path('SAC/', DoctorView.get_specializations, name='specialization_autocomplete'),
    path('AAC/', DoctorView.get_accreditations, name='accreditation_autocomplete')
]
