from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('name',
                'doctor_registeration_no',
                'email',
                'phone_number',
                'experience',
                'affiliation',
                'accrediation',
                'address',
                'adharcardno',
                'specialization',)
