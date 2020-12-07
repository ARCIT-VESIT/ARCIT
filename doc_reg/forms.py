from django import forms
from .models import Doctor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class DoctorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100,required=True, help_text='It is required')
    last_name = forms.CharField(max_length=100,required=True, help_text='It is required')
    doctor_registeration_no = forms.CharField(max_length = 30,required=True, help_text='It is required')
    email = forms.EmailField(max_length=254,required=True, help_text='It is required')
    phone_number = forms.IntegerField()
    experience = forms.IntegerField(required=True, help_text='It is required')
    affiliation = forms.CharField(max_length=100, required=True, help_text='It is required')
    accrediation = forms.CharField(max_length=254,required=True, help_text='It is required')
    address = forms.CharField(max_length=100,required=True, help_text='It is required')
    adharcardno = forms.IntegerField(required=True, help_text='It is required')
    specialization = forms.CharField(max_length=100,required=True, help_text='It is required')

    class Meta:
        model = Doctor
        fields = ('first_name','last_name','doctor_registeration_no','email','phone_number','experience','affiliation','accrediation','address','adharcardno','specialization',)

    # class Meta:
    #     userModel = User
    #     fields = ('username', 'password1', )


class DoctorUserForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', )