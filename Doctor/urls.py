"""Url for doctor"""
from django.urls import path
from django.conf.urls import url
from Doctor import views as DoctorViews

urlpatterns = [
    url(r'^d/profile/$',
        DoctorViews.ViewDoctorProfile.as_view(template_name='Doctor/profile.html'),
        name='doctorprofile'),
    url(r'^p/addDiagnosis/$',
        DoctorViews.AddPatientDataView.as_view(template_name='Doctor/addPatientHistory.html'),
        name='PatientHistory'),
    url(r'^p/history/a$',
        DoctorViews.ViewPatientHistory.as_view(template_name='Patient/addEditHistory.html'),
        name='addPatientRecord'),
    path('SAC/', DoctorViews.get_specializations, name='specialization_autocomplete'),
    path('AAC/', DoctorViews.get_accreditations, name='accreditation_autocomplete')
]
