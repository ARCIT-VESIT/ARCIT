from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from ARCIT.models import UserTypeModel
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', )

class UserTypeForm(ModelForm):
    class Meta:
        model = UserTypeModel
        fields = ['usertype']