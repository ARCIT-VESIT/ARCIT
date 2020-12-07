from django import forms
from PatientHistory.models import PatientHistory
from django.contrib.auth.forms import UserCreationForm



class PatientHistori(forms.ModelForm):
    #username = forms.CharField(max_length=30, required=True, help_text='required.')
    medical_status = forms.CharField(max_length=50)
    symtomps = forms.CharField(max_length=1000)
    disease	= forms.CharField(max_length=200)
    affected_area = forms.CharField(max_length=200)
    #report = forms.FileField( max_length=500, required=True)
    timespan = forms.CharField(max_length=100)
    precription = forms.CharField(max_length=1000)
    course_duration = forms.CharField(max_length=100)
    follow_up = forms.CharField(max_length=100,required=True)
    referred_from = forms.CharField(max_length=100,required=True)
    referred_to= forms.CharField(max_length=100,required=True)

    class Meta:
        model =  PatientHistory
        fields = ('medical_status', 'symtomps', 'disease', 'affected_area','timespan','precription','course_duration','follow_up','referred_from','referred_to', )


