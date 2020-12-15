from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.urls import path
from . import views
from Hospital.views import FilteredDoctorListView, HospitalView, HospitalProfileView

urlpatterns = [
    # url(r'^hospitalIndex/$', IndexView.as_view(template_name='Hospital/index.html'), name='hospitalIndex'),
    url(r'^h/doctors/$', FilteredDoctorListView.as_view(template_name='Hospital/index2.html'), name='hospitaldoctors'),
    url(r'^h/index/$', HospitalView.as_view(template_name='Hospital/index.html'), name='HospitalIndex'),
    url(r'^h/profile/$', HospitalProfileView.as_view(template_name='Hospital/profile.html'), name='hospitalprofile'),
    url(r'^HospitalRegisteration/$', HospitalView.as_view(template_name='HospitalRegisteration.html'), name='HospitalRegisteration'),
]