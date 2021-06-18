from django import forms
from DiagnosticDepartment.models import DiagnosticDepartment, DiagnosticDepartmentReport
from django.contrib.auth import get_user_model

class DiagnosticDepartmentForm(forms.ModelForm):
    class Meta:
        model = DiagnosticDepartmentReport
        fields = ('id', 'name', 'supervisor', 'referred_by', 'report', )

class DiagnosticDepartmentSignupForm(forms.ModelForm):
    affiliation = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'autocomplete':'off',
            'data-url': "/HAC",
        }))

    def clean_affiliation(self):
        data = self.cleaned_data.get("affiliation")
        if not get_user_model().objects.all().filter(is_hospital=True).only("username").filter(username=data):
            raise forms.ValidationError(("Hospital does not exist"), code='invalid')
        return data

    class Meta:
        model = DiagnosticDepartment
        fields = ('name','DD_type', 'DD_license', 'affiliation','address','email','website','registeration_number','phone_number','specialization',)