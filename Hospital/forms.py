"""Form for hospital"""
from django import forms
from .models import Hospital

class HospitalForm(forms.ModelForm):
    '''Hospital reigsteration form'''

    class Meta:
        model = Hospital
        fields = ('name',
                  'address',
                  'email',
                  'website',
                  'registeration_number',
                  'phone_number',
                  'specialization',)
