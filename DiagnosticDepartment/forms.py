from django import forms
from DiagnosticDepartment.models import DiagnosticDepartment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from DiagnosticDepartment.models import  DiagnosticDepartmentReport


class DiagnosticDepartmentForm(forms.ModelForm):
    # name = forms.CharField(max_length=100, help_text= 'It is required')
    # DD_type = forms.CharField(max_length=100, help_text= 'It is required')
    # DD_license = forms.CharField(max_length=100, help_text= 'It is required')
    # affiliation = forms.CharField(max_length=100, help_text= 'It is required')
    # supervisor = forms.CharField(max_length=100, help_text= 'It is required')
    # referred_by = forms.CharField(max_length=100, help_text= 'It is required')
    # handled_by = forms.CharField(max_length=100, help_text= 'It is required')
    # patient_name = forms.CharField(max_length=100, help_text= 'It is required')
    # report = forms.FileField()
    class Meta:
        model = DiagnosticDepartmentReport
        # fields = ['name', 'DD_type', 'DD_license', 'affiliation','supervisor','referred_by','handled_by','patient_name','report'] 
        # fields = ['name', 'supervisor','referred_by','handled_by','patient_name','report'] 
        fields = '__all__'

class DiagnosticDepartmentSignupForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text= 'It is required')
    DD_type = forms.CharField(max_length=100, help_text= 'It is required')
    DD_license = forms.CharField(max_length=100, help_text= 'It is required')
    affiliation = forms.CharField(max_length=100, help_text= 'It is required')
    name = forms.CharField(max_length=100,required=True, help_text='It is required')
    address = forms.CharField(max_length=100,required=True, help_text='It is required')
    email = forms.EmailField(max_length=254,required=True, help_text='It is required')
    website = forms.CharField(max_length=100, required=True, help_text='It is required')
    registeration_number = forms.IntegerField()
    phone_number = forms.IntegerField()
    specialization = forms.CharField(max_length=100,required=True, help_text='It is required')

    class Meta:
        model = DiagnosticDepartment
        # fields = '__all__'
        fields = ('name','DD_type', 'DD_license', 'affiliation','address','email','website','registeration_number','phone_number','specialization',)

class DiagnosticDepartmentUserForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', )