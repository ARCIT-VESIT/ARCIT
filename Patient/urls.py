"""Urls for patient"""
from django.conf.urls import url
from django.urls import path

from Patient import views as PatientView


urlpatterns = [
   # url(r'^patreg/$', auth_views.LogoutView.as_view(template_name='patreg.html'), name='logout')
   url(r'^p/signup/$',
      PatientView.PatientRegisterationView.as_view(template_name='Patient/registeration.html'),
      name='patreg'),
   url(r'^p/profile/$',
      PatientView.ViewPatientProfile.as_view(template_name='Patient/profile.html'),
      name='patientprofile'),
   url(r'^p/viewHistory/$',
      PatientView.ViewPatientHistory.as_view(template_name='Patient/viewHistory.html'),
      name='viewHistory'),
   url(r'^p/viewReports_p/$',
      PatientView.ViewPatientReports.as_view(template_name='Patient/viewReport.html'),
      name='viewReport_p'),
   path('PatientHistory/',
      PatientView.ViewPatientHistory.as_view(template_name='Patient/viewHistory.html'),
      name='PatientHistoryUpload'),
]
