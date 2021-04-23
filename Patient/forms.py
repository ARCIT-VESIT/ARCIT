from django import forms
from .models import  Patient, PatientHistory

class UserRegisterationForm(forms.ModelForm):
    class Meta:
        model =  Patient
        fields = ('name',
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
