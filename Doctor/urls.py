"""Url for doctor"""
from django.urls import path
from django.conf.urls import url
from Doctor import views as DoctorView

urlpatterns = [
    url(r'^d/profile/$',
        DoctorView.ViewDoctorProfile.as_view(template_name='Doctor/profile.html'),
        name='doctorprofile'),
    url(r'^p/addDiagnosis/$',
        DoctorView.AddPatientDataView.as_view(template_name='Doctor/addPatientHistory.html'),
        name='PatientHistory'),
    path('d/A2Oredirect/<int:id>', 
        DoctorView.A2Oredirect.as_view(template_name="Authentication/otp.html"),
        name='A20redirect'),
    path('d/dashboard/', DoctorView.dashboard, name='doctor_dashboard'),
    path('d/appointments/', DoctorView.appointments, name='doctorAppointments'),
    path('d/dashboard_data', DoctorView.dashboard_data, name='doctor_dashboard_data'),
    path('d/patient_treated', DoctorView.dashboard_data, name='patient_treated'),
    path('d/profile/set_active_hour', DoctorView.set_active_hour, name='set_active_hour'),
    path('d/profile/delete_active_hour', DoctorView.delete_active_hour, name='delete_active_hour'),
    path('SAC/', DoctorView.get_specializations, name='specialization_autocomplete'),
    path('AAC/', DoctorView.get_accreditations, name='accreditation_autocomplete')
]
