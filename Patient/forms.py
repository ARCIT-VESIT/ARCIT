from django import forms
from .models import  Patient, PatientHistory

class RegForm(forms.ModelForm):
    class Meta:
        model =  Patient
        fields = ('first_name',
                'last_name',
                'email',
                'phone_number',
                'dob',
                'gender',
                'weight',
                'address',
                'adharcardno',
                'blood_group',)

class PatientHistoryForm(forms.ModelForm):
    class Meta:
        model =  PatientHistory
        fields = ('medical_status',
                'symtomps',
                'disease',
                'affected_area',
                'timespan',
                'prescription',
                'course_duration',
                'follow_up',
                'referred_to',)
