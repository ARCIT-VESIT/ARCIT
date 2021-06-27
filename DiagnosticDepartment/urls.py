from django.conf.urls import url
from django.urls import path

from DiagnosticDepartment import views as DDViews

urlpatterns = [
   path('RTAC/', DDViews.get_report_types, name='report_types_autocomplete'),
   path('DiagnosticDepartment/<int:id>', DDViews.DiagnosticDepartmentUploadReport.as_view(template_name = "DiagnosticDepartment/UploadReport.html"), name='DiagnosticDepartmentUpload'),
   url(r'^dd/profile$', DDViews.ViewDiagnosticDepartment.as_view(template_name = "DiagnosticDepartment/profile.html"), name='ddprofile'),
]