from django.conf.urls import url
from django.contrib import admin
from patregistration.views import docregister
from django.views.generic.base import TemplateView



urlpatterns = [
   # url(r'^patreg/$', auth_views.LogoutView.as_view(template_name='patreg.html'), name='logout')
   url(r'^patreg/$', docregister.as_view(template_name='patreg.html'), name='patreg'),


   
]

