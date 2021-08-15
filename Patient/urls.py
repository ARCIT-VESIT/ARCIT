"""Urls for patient"""
from django.conf.urls import url
from django.urls import path

from Patient import views as PatientViews

urlpatterns = [
   url(r'^p/profile/$',
      PatientViews.ViewPatientProfile.as_view(template_name='Patient/profile.html'),
      name='patientprofile'),
   url(r'^p/history/v/$',
      PatientViews.ViewPatientHistory.as_view(template_name='Patient/addEditHistory.html'),
      name='viewHistory'),
   path('p/dashboard/', PatientViews.dashboard, name='patient_dashboard'),
   path('p/dashboard_data', PatientViews.dashboard_data, name='patient_dashboard_data'),
   path('news/', PatientViews.get_news, name='trending_news'),
   path('PSAC/', PatientViews.get_states, name='state_autocomplete'),
]
