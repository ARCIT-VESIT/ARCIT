from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from DiagnosticDepartment.views import DiagnosticLoginView

urlpatterns = [
   path('DiagnosticDepartment/', views.upload, name='DiagnosticDepartmentUpload'),
   url(r'^dd/signup$', DiagnosticLoginView.as_view(template_name = "DiagnosticDepartment/signup.html"), name='ddsignup'),
]