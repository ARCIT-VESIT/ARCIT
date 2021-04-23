from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

User = get_user_model()

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            request.session['loggedin_username'] = username

            user = authenticate(username=username, password=password)
            if user.is_doctor:
                request.session['role'] = 'Doctor'
                request.session['is_doctor'] = True
                return redirect('doctorprofile')
            elif user.is_patient:
                request.session['role'] = 'Patient'
                request.session['is_patient'] = True
                return redirect('patientprofile')
            elif user.is_hospital:
                request.session['role'] = 'Hospital'
                request.session['is_hospital'] = True
                return redirect('hospitalprofile')
            elif user.is_diagnosticDepartment:
                request.session['role'] = 'DD'
                request.session['is_dd'] = True
                return redirect('ddprofile')
        else:
            return render(request, 'Authentication/login.html', {'form': form})
    else:
        form = AuthenticationForm(request)
    return render(request, 'Authentication/login.html', {'form': form})
