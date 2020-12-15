from django import forms
from .models import  Patients
from ARCIT.models import User
from .models import PatientHistory
from django.contrib.auth.forms import UserCreationForm

class RegForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)
    #phone_number=forms.NumberInput(=12,required=True,help_text='')
    phone_number=forms.IntegerField()
    dob=forms.DateField()
    gender=forms.CharField(max_length=30, required=True)
    weight=forms.IntegerField()
    address=forms.CharField(max_length=30, required=True)
    adharcardno=forms.IntegerField()
    blood_group=forms.CharField(max_length=30, required=False)

    class Meta:
        model =  Patients
        fields = ('first_name', 'last_name', 'email', 'phone_number','dob','gender','weight','address','adharcardno','blood_group', )

class PatUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )


class PatientHistoryForm(forms.ModelForm):
    #username = forms.CharField(max_length=30, required=True, help_text='required.')
    medical_status = forms.CharField(max_length=50)
    symtomps = forms.CharField(max_length=1000)
    disease	= forms.CharField(max_length=200)
    affected_area = forms.CharField(max_length=200)
    #report = forms.FileField()
    timespan = forms.CharField(max_length=100)
    precription = forms.CharField(max_length=1000)
    course_duration = forms.CharField(max_length=100)
    follow_up = forms.CharField(max_length=100,required=True)
    referred_from = forms.CharField(max_length=100,required=True)
    referred_to= forms.CharField(max_length=100,required=True)

    class Meta:
        model =  PatientHistory
        fields = ('medical_status', 'symtomps', 'disease', 'affected_area','timespan','precription','course_duration','follow_up','referred_from','referred_to', )