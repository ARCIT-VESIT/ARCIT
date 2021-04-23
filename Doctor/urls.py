"""Url for doctor"""
from django.conf.urls import url
from Doctor import views as DoctorViews

urlpatterns = [
    url(r'^d/signup/$',
        DoctorViews.DoctorView.as_view(template_name='Doctor/registeration.html'),
        name='docreg'),
    url(r'^d/profile/$',
        DoctorViews.ViewDoctorProfile.as_view(template_name='Doctor/profile.html'),
        name='doctorprofile'),
    url(r'^p/reports/$',
        DoctorViews.ViewPatientReports.as_view(template_name='Doctor/viewPatientReport.html'),
        name='PatientReports'),
    url(r'^p/addDiagnosis/$',
        DoctorViews.AddPatientDataView.as_view(template_name='Doctor/addPatientHistory.html'),
        name='PatientHistory'),
    url(r'^p/history/$',
        DoctorViews.ViewPatientHistory.as_view(template_name='Doctor/viewPatientHistory.html'),
        name='viewpatienthistory'),
]
