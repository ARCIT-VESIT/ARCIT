from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from ARCIT.forms import MyModelForm, SignUpForm,UserTypeForm
from ARCIT.models import MyModel,UserTypeModel

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class CreateMyModelView(CreateView):
    model = MyModel
    form_class = MyModelForm
    template_name = 'template.html'


class UserTypeView(CreateView):
    model = UserTypeModel
    form_class = UserTypeForm
    template_name = 'home1.html'

    def get(self, request):
        return render(request, self.template_name, {'form123': self.form_class})

    def post(self, request):
        if request.POST['usertype'] == '1':
            return redirect('patreg')
        elif request.POST['usertype'] == '2':
            return redirect('docreg')
        else:
            return render(request, self.template_name)
