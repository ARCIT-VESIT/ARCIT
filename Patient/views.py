# from datetime import date, datetime

from django.contrib.auth import authenticate, get_user_model, login
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from otpAuth.views import OtpAuthView, VerifyOtpView

from .forms import PatientHistoryForm, PatUserForm, RegForm
from .models import PatientHistory, Patients
from DiagnosticDepartment.models import DiagnosticDepartmentReport

User = get_user_model()

def upload(request):
    form = PatientHistoryForm()
    context = {}
    context['form'] = form

    if request.method == 'POST':
        form = PatientHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            data=form.save(commit=True)
            url = data.report.url
            print(url)
        return render(request, 'Doctor/addPatientHistory.html', {'msg': "file uploaded successfully", 'url':url})

    return render(request, 'Doctor/addPatientHistory.html', context) 

class PatientRegisterationView(TemplateView):
    template_name='Patient/registeration.html'

    def get(self,request):
        form = RegForm()
        form2 = PatUserForm()

        return render(request,self.template_name,{'form':form, 'form2': form2  } )

    def post(self,request):
        if request.method == 'POST':
            form = PatUserForm(request.POST)
            form2 = RegForm(request.POST)

            if form.is_valid() and form2.is_valid():

                user = User.objects.create_user(
                    form.data['username'],
                    form2.data['email'],
                    form.data['password1'],
                    first_name=form2.data['first_name'],
                    last_name=form2.data['last_name'],
                    is_patient = True
                )

                patform=form2.save(commit=False)
                patform.user=user
                patform.save()

                # user = authenticate(username=form2.data['username'], password=form2.data['password1'])
                # login(request, user)
                if User.is_doctor:
                    return redirect('otpIndex')
                else:
                    return redirect('login')
            else:
                form = PatUserForm()
                form2=RegForm()
            return render(request,self.template_name, {'form': form,'form2':form2})

class ViewPatientProfile(TemplateView):
    template_name='Patient/profile.html'

    def get(self,request):        
        user = User.objects.get(username=request.session['loggedin_username'])
        print(user)
        patient = Patients.objects.get(user=user)
        # today = date.today()
        # age = today.year - datetime.year(patient.dob) - ((today.month, today.day) < (datetime.month(patient.dob), datetime.day(patient.dob)))
        # age = patient.dob
        return render(request,self.template_name,{'profile':patient})


class ViewPatientHistory(TemplateView):
    template_name='Patient/viewHistory.html'

    def get(self,request):
        user = User.objects.get(username=request.session['loggedin_username'])
        model = PatientHistory.objects.filter(user=user)

        return render(request,self.template_name,{'models':model})

class ViewPatientReports(TemplateView):
    template_name='Patient/viewReports_p.html'

    def get(self,request):
        user = User.objects.get(username=request.session['loggedin_username'])
        model = DiagnosticDepartmentReport.objects.filter(user=user)

        return render(request,self.template_name,{'models':model})
