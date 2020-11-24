from django import forms
from ARCIT.models import  Patients


class RegForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    #phone_number=forms.NumberInput(=12,required=True,help_text='')
    phone_number=forms.IntegerField()
    dob=forms.DateField()
    gender=forms.CharField(max_length=30, required=True, help_text='Optional.')
    weight=forms.IntegerField()
    address=forms.CharField(max_length=30, required=True, help_text='Optional.')
    adharcardno=forms.IntegerField()
    blood_group=forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model =  Patients
        fields = ('first_name', 'last_name', 'email', 'phone_number','dob','gender','weight','address','adharcardno','blood_group', )
