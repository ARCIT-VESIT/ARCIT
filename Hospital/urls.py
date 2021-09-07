"""Hospital Urls"""
from django.conf.urls import url
from django.urls import path
from Hospital import views as HospitalViews

urlpatterns = [
    url(r'^h/profile/$',
        HospitalViews.HospitalProfileView.as_view(template_name='Hospital/profile.html'),
        name='hospitalprofile'),
    path('h/doctors/',HospitalViews.AffiliatedDoctors,name='hospitaldoctors'),
    path('HAC/', HospitalViews.get_hospitals, name='hospital_autocomplete'),
    path('HSAC/', HospitalViews.get_hospital_specializations, name='hospital_speciality_autocomplete'),
    path('h/set_appointment', HospitalViews.set_appointment, name='setAppointmentByH'),
]
