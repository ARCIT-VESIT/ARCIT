from django.conf.urls import url
from Doctor.views import DoctorView,ViewDocotrProfile, ViewPatientReports, AddPatientDataView, ViewPatientHistory

urlpatterns = [
    url(r'^d/signup/$', DoctorView.as_view(template_name='Doctor/registeration.html'), name='docreg'),
    url(r'^d/profile/$', ViewDocotrProfile.as_view(template_name='Doctor/profile.html'), name='doctorprofile'),
    url(r'^p/reports/$', ViewPatientReports.as_view(template_name='Doctor/viewPatientReport.html'), name='PatientReports'),
    url(r'^p/addDiagnosis/$', AddPatientDataView.as_view(template_name='Doctor/addPatientHistory.html'), name='PatientHistory'),
    url(r'^p/history/$', ViewPatientHistory.as_view(template_name='Doctor/viewPatientHistory.html'), name='viewpatienthistory'),
]
