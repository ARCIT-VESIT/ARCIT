from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.urls import path
from . import views
from Hospital.views import FilteredDoctorListView, HospitalView 

urlpatterns = [
    # url(r'^hospitalIndex/$', IndexView.as_view(template_name='Hospital/index.html'), name='hospitalIndex'),
    url(r'^h/index/$', FilteredDoctorListView.as_view(template_name='Hospital/index2.html'), name='HI'),
    url(r'^HospitalRegisteration/$', HospitalView.as_view(template_name='HospitalRegisteration.html'), name='HospitalRegisteration'),
]