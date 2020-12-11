import django_filters
from Doctor.models import Doctor

class DoctorFilter(django_filters.FilterSet):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization']
        # fields = ['first_name', 'last_name', 'doctor_register', 'email', 'phone_number', 'experience', 'affiliation', 'accrediation', 'address', 'adharcardno', 'specialization']