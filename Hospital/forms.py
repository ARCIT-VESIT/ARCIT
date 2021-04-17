"""Form for hospital"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Hospital


class HospitalForm(forms.ModelForm):
    '''Hospital reigsteration form'''
    name = forms.CharField(max_length=100,required=True, help_text='It is required')
    address = forms.CharField(max_length=100,required=True, help_text='It is required')
    email = forms.EmailField(max_length=254,required=True, help_text='It is required')
    website = forms.CharField(max_length=100, required=True, help_text='It is required')
    registeration_number = forms.IntegerField()
    phone_number = forms.IntegerField()
    specialization = forms.CharField(max_length=100,required=True, help_text='It is required')

    class Meta:
        model = Hospital
        fields = ('name',
                  'address',
                  'email',
                  'website',
                  'registeration_number',
                  'phone_number',
                  'specialization',)

    # class Meta:
    #     userModel = User
    #     fields = ('username', 'password1', )


class HospitalUserForm(UserCreationForm):
    '''Hospital registeration user form'''

    class Meta:
        '''Meta information about hospital registeration user form'''

        model = get_user_model()
        fields = ('username', 'password1', 'password2', )
