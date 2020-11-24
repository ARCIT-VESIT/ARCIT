from django import forms

class OtpAuthForm(forms.Form):
    Phone_number = forms.IntegerField()
    otp = forms.IntegerField(required=False)
    # otp = forms.IntegerField(widget=forms.HiddenInput(), required=False)