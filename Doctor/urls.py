from django.conf.urls import url
from Doctor.views import DoctorView,ViewDocotrProfile

urlpatterns = [
    url(r'^docreg/$', DoctorView.as_view(template_name='doc_reg.html'), name='docreg'),
    url(r'^d/profile/$', ViewDocotrProfile.as_view(template_name='Doctor/profile.html'), name='doctorprofile'),
]
