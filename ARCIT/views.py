from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect

from ARCIT.forms import  SignUpForm,UserTypeForm
from ARCIT.models import UserTypeModel

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

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            request.session['loggedin_username'] = username

            user = authenticate(username=username, password=password)
            
            if user.is_doctor:
                # return render(request, 'Doctor/index.html')
                return render(request, 'Doctor/index1.html')
            elif user.is_patient:
                return render(request, 'Patient/index1.html')
                # return redirect('patientprofile')
            elif user.is_hospital:
                # return render(request, 'Hospital/index2.html')
                return redirect('HospitalIndex')
            elif user.is_diagnosticDepartment:
                return render(request, 'DiagnosticDepartment/index.html')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})


class UserTypeView(CreateView):
    model = UserTypeModel
    form_class = UserTypeForm
    template_name = 'home1.html'

    def get(self, request):
        return render(request, self.template_name, {'form123': self.form_class})

    def post(self, request):
        # if request.POST['usertype'] == '1':
        #     return redirect('patreg')
        if request.POST['usertype'] == '2':
            return redirect('docreg')
        elif request.POST['usertype'] == '3':
            return redirect('HospitalRegisteration')
        elif request.POST['usertype'] == '4':
            return redirect('ddsignup')
        else:
            return render(request, self.template_name)
