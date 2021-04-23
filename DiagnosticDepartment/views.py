# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate

from Patient.models import Patient
from ARCIT.forms import UserForm
from .forms import DiagnosticDepartmentForm, DiagnosticDepartmentSignupForm
from .models import DiagnosticDepartment

User = get_user_model()

class DiagnosticDepartmentUploadReport(TemplateView):
    def get(self, request, *args, **kwargs):
        form = DiagnosticDepartmentForm()
        context = {}
        context['form'] = form
        return render(request, 'DiagnosticDepartment/UploadReport.html', context)

    def post(self, request):
        
        form = DiagnosticDepartmentForm()
        context = {}
        context['form'] = form

        if request.method == 'POST':
            form = DiagnosticDepartmentForm(request.POST, request.FILES)
            if form.is_valid():
                user = Patient.objects.get(phone_number=request.session['phoneNumber']).user
                dd_user = User.objects.get(username=request.session['loggedin_username'])

                ddForm=form.save(commit=False)
                ddForm.user=user
                ddForm.handled_by=dd_user
                ddForm.save()
                url = ddForm.report.url
                
                return render(request, 'DiagnosticDepartment/UploadReport.html', {'msg': "file uploaded successfully", 'url':url})

        return render(request, 'DiagnosticDepartment/UploadReport.html', context)

class DiagnosticLoginView(TemplateView):
    template_name='Hospital/registeration.html'

    def get(self, request, *args, **kwargs):
        '''request to handle get registeration of DD form'''
        form = DiagnosticDepartmentSignupForm()
        form2 = UserForm()
        return render(request,self.template_name,{'form':form, 'form2': form2})

    def post(self,request):
        '''request to handle post registeration of DD form'''
        form =  UserForm(request.POST)
        form2 = DiagnosticDepartmentSignupForm(request.POST)

        if form.is_valid() and form2.is_valid():
            user = User.objects.create_user(
                form.data['username'],
                form2.data['email'],
                form.data['password1'],
                first_name=form2.data['name'],
                is_diagnosticDepartment = True,
            )

            diagnostic_department_form=form2.save(commit=False)
            diagnostic_department_form.user=user
            diagnostic_department_form.save()

            user = authenticate(username=form2.data['username'], password=form2.data['password1'])
            login(request, user)
            return redirect('login')
        else:
            form =  DiagnosticDepartmentSignupForm(request.POST)
            form2 = UserForm(request.POST)
            return render(request,self.template_name, {'form': form,'form2':form2})

class ViewDiagnosticDepartment(TemplateView):
    template_name='DiagnosticDepartment/profile.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        print(user)
        diagnosticdepartment = DiagnosticDepartment.objects.get(user=user)

        return render (request,self.template_name,{'profile':diagnosticdepartment})