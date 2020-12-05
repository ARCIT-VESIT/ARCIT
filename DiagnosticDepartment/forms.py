from django import forms
from ARCIT.models import DiagnosticDepartment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# class UserHistoryForm(forms.ModelForm):
    

#     class Meta:
#         model = DiagnosticDepartment
#         fields = ('report',)

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
        model = DiagnosticDepartment
        fields = ['name', 'DD_type', 'DD_license', 'affiliation','supervisor','referred_by','handled_by','patient_name','report'] 




