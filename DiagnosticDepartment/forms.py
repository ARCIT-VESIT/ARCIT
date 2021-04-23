from django import forms
from DiagnosticDepartment.models import DiagnosticDepartment

from DiagnosticDepartment.models import  DiagnosticDepartmentReport


class DiagnosticDepartmentForm(forms.ModelForm):
    class Meta:
        model = DiagnosticDepartmentReport
        fields = ('id', 'name', 'supervisor', 'referred_by', 'report', )

class DiagnosticDepartmentSignupForm(forms.ModelForm):
    class Meta:
        model = DiagnosticDepartment
        fields = ('name','DD_type', 'DD_license', 'affiliation','address','email','website','registeration_number','phone_number','specialization',)