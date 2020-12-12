from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView

from .views import PatientRegisterationView, AddPatientDataView, ViewPatientHistory, ViewPatientProfile,ViewPatientHistory_p


urlpatterns = [
   # url(r'^patreg/$', auth_views.LogoutView.as_view(template_name='patreg.html'), name='logout')
   url(r'^patreg/$', PatientRegisterationView.as_view(template_name='patreg.html'), name='patreg'),
   url(r'^p/addDiagnosis/$', AddPatientDataView.as_view(template_name='PatientHistory.html'), name='PatientHistory'),
   url(r'^p/history/$', ViewPatientHistory.as_view(template_name='Patient/viewHistory.html'), name='viewpatienthistory'),
   url(r'^p/profile/$', ViewPatientProfile.as_view(template_name='Patient/profile.html'), name='patientprofile'),
   url(r'^p/viewHistory_p/$', ViewPatientHistory_p.as_view(template_name='Patient/viewHistory_p.html'), name='viewHistory_p'),
]