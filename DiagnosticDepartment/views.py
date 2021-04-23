# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from Patient.models import Patient
from .forms import DiagnosticDepartmentForm
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

                form_data=form.save(commit=False)
                form_data.user=user
                form_data.handled_by=dd_user
                form_data.save()
                url = form_data.report.url
                
                return render(request, 'DiagnosticDepartment/UploadReport.html', {'msg': "file uploaded successfully", 'url':url})

        return render(request, 'DiagnosticDepartment/UploadReport.html', context)

class ViewDiagnosticDepartment(TemplateView):
    template_name='DiagnosticDepartment/profile.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        print(user)
        diagnosticdepartment = DiagnosticDepartment.objects.get(user=user)

        return render (request,self.template_name,{'profile':diagnosticdepartment})