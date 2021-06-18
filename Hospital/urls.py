"""Hospital Urls"""
from django.conf.urls import url
from django.urls import path
from Hospital import views as HospitalViews

urlpatterns = [
    url(r'^h/doctors/$',
        HospitalViews.FilteredDoctorListView.as_view(
            template_name='Hospital/affiliatedDoctors.html'),
        name='hospitaldoctors'),
    url(r'^h/profile/$',
        HospitalViews.HospitalProfileView.as_view(template_name='Hospital/profile.html'),
        name='hospitalprofile'),
    path('HAC/', HospitalViews.get_hospitals, name='hospital_autocomplete')
]
