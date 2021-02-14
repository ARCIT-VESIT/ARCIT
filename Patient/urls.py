from django.conf.urls import url
from django.urls import path

from .views import PatientRegisterationView, ViewPatientProfile,ViewPatientHistory, ViewPatientReports


urlpatterns = [
   # url(r'^patreg/$', auth_views.LogoutView.as_view(template_name='patreg.html'), name='logout')
   url(r'^p/signup/$', PatientRegisterationView.as_view(template_name='Patient/registeration.html'), name='patreg'),
   url(r'^p/profile/$', ViewPatientProfile.as_view(template_name='Patient/profile.html'), name='patientprofile'),
   url(r'^p/viewHistory/$', ViewPatientHistory.as_view(template_name='Patient/viewHistory.html'), name='viewHistory'),
   url(r'^p/viewReports_p/$', ViewPatientReports.as_view(template_name='Patient/viewReport.html'), name='viewReport_p'),
   path('PatientHistory/',  ViewPatientHistory.as_view(template_name='Patient/viewHistory.html'), name='PatientHistoryUpload'),
]
