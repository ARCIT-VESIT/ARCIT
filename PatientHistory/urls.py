from django.conf.urls import url
from django.contrib import admin
from PatientHistory.views import PatientHistore
from django.views.generic.base import TemplateView



urlpatterns = [
   
   url(r'^PatientHistory/$', PatientHistore.as_view(template_name='PatientHistory.html'), name='PatientHistory'),


   
]

