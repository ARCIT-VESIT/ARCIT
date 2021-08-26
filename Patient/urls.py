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
   path('p/appointments/', PatientViews.upcomingAppointments, name='upcomingAppointments'),
   path('d/appointment/', PatientViews.doctor_appointment, name='requestAppointment'),
   path('d/set_appointment', PatientViews.set_appointment, name='setAppointment'),
   path('p/dashboard/', PatientViews.dashboard, name='patient_dashboard'),
   path('p/most_visited_specialities', PatientViews.most_visited_specialities, name='patient_most_visited_specialities'),
   path('p/frequent_diseases', PatientViews.frequent_diseases, name='patient_frequent_diseases'),
   path('news/', PatientViews.get_news, name='trending_news'),
   path('PSAC/', PatientViews.get_states, name='state_autocomplete'),
]
