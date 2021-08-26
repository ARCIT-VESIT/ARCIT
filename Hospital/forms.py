"""Form for hospital"""
from django import forms
from .models import Hospital

class HospitalRegisterationForm(forms.ModelForm):
    '''Hospital reigsteration form'''
    specialization = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'autocomplete':'off',
            'data-url': "/HSAC",
        }))

    class Meta:
        model = Hospital
        fields = ('name',
                  'address',
                  'email',
                  'website',
                  'registeration_number',
                  'phone_number',
                  'specialization',)
