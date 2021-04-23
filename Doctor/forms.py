from django import forms
from .models import Doctor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('first_name',
                'last_name',
                'doctor_registeration_no',
                'email',
                'phone_number',
                'experience',
                'affiliation',
                'accrediation',
                'address',
                'adharcardno',
                'specialization',)


class DoctorUserForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', )