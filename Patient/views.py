# from datetime import date, datetime
"""View for patient"""
from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic import TemplateView

from DiagnosticDepartment.models import DiagnosticDepartmentReport
from .forms import PatientHistoryForm
from .models import PatientHistory, Patient

User = get_user_model()

def upload(request):
    '''Method to upload patient reports'''
    form = PatientHistoryForm()
    context = {}
    context['form'] = form

    if request.method == 'POST':
        form = PatientHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            data=form.save(commit=True)
            url = data.report.url
            print(url)
        return render(request,
                    'Doctor/addPatientHistory.html',
                    {'msg': "file uploaded successfully", 'url':url})

    return render(request, 'Doctor/addPatientHistory.html', context)

class ViewPatientProfile(TemplateView):
    '''view for patient to view their profile'''
    template_name='Patient/profile.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        print(user)
        patient = Patient.objects.get(user=user)
        # today = date.today()
        # age = today.year - datetime.year(patient.dob) - ((today.month, today.day)
        #       < (datetime.month(patient.dob), datetime.day(patient.dob)))
        # age = patient.dob
        return render(request,self.template_name,{'profile':patient})


class ViewPatientHistory(TemplateView):
    '''For patient to view their history'''
    template_name='Patient/viewHistory.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        model = PatientHistory.objects.filter(user=user).order_by("-created_on")

        return render(request,self.template_name,{'models':model})

class ViewPatientReports(TemplateView):
    '''For patient to view their reports'''
    template_name='Patient/viewReports_p.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        model = DiagnosticDepartmentReport.objects.filter(user=user).order_by("-created_on")

        return render(request,self.template_name,{'models':model})
