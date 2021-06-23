from django import forms
from .models import Doctor
from django.contrib.auth import get_user_model

class DoctorForm(forms.ModelForm):
    affiliation = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'autocomplete':'off',
            'data-url': "/HAC"
        }))
    specialization = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'autocomplete':'off',
            'data-url': "/SAC"
        }))
    accreditation = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'autocomplete':'off',
            'data-url': "/AAC"
        }))

    def clean_affiliation(self):
        data = self.cleaned_data.get("affiliation")
        if not get_user_model().objects.all().filter(is_hospital=True).only("username").filter(username=data):
            raise forms.ValidationError(("Hospital does not exist"), code='invalid')
        return data

    class Meta:
        model = Doctor
        fields = ('name',
                'doctor_registeration_no',
                'email',
                'phone_number',
                'experience',
                'affiliation',
                'accreditation',
                'specialization',
                'address',
                'adharcardno',)
