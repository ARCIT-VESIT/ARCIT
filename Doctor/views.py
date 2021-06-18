"""View for Doctor"""
import json
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from DiagnosticDepartment.models import DiagnosticDepartmentReport
from Patient.models import Patient, PatientHistory
from Patient.forms import PatientHistoryForm
from .models import Doctor

User = get_user_model()

class ViewDoctorProfile(TemplateView):
    '''View for doctor profile'''
    template_name='Doctor/profile.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        print(user)
        doctor = Doctor.objects.get(user=user)
        # today = date.today()
        # age = today.year - datetime.year(patient.dob) - ((today.month, today.day)
        #       < (datetime.month(patient.dob), datetime.day(patient.dob)))
        # age = patient.dob
        return render(request,self.template_name,{'profile':doctor})

class ViewPatientReports(TemplateView):
    '''For doctors to view patient reports'''
    template_name='Doctor/viewPatientReport.html'

    def get(self,request, *args, **kwargs):
        user = Patient.objects.get(phone_number=request.session['phoneNumber']).user
        model = DiagnosticDepartmentReport.objects.filter(user=user).order_by("-created_on")

        return render(request,self.template_name,{'models':model})


class AddPatientDataView(TemplateView):
    '''For doctors to add new patient'''
    template_name='Doctor/addPatientHistory.html'

    def get(self,request, *args, **kwargs):
        form = PatientHistoryForm()

        return render(request,self.template_name,{'form':form})

    def post(self,request):
        '''Post method to add patient history'''
        form=PatientHistoryForm(request.POST)

        user = Patient.objects.get(phone_number=request.session['phoneNumber']).user
        doctor_user = User.objects.get(username=request.session['loggedin_username'])

        if form.is_valid():
            formdata = form.save(commit=False)
            formdata.user=user
            formdata.referred_from = doctor_user
            formdata.save()

            # return render(request, 'Doctor/index.html')
            return redirect('viewpatienthistory')
        form = PatientHistoryForm()
        return render(request,self.template_name, {'form': form})

class ViewPatientHistory(TemplateView):
    '''Class for doctor to view the patient history'''
    template_name='Doctor/viewPatientHistory.html'

    def get(self,request, *args, **kwargs):
        user = Patient.objects.get(phone_number=request.session['phoneNumber']).user
        model = PatientHistory.objects.filter(user=user).order_by("-created_on")

        return render(request,self.template_name,{'models':model})

def get_specializations(request):
    try:
        with open("static/autocomplete_data/specializations.json", 'r') as f:
            data = json.load(f)
            
            if request.GET.get('q'):
                query = request.GET['q']

                filtered_list = list(filter(lambda x: query in x.lower(), data))
                filtered_list.sort()
                
                return JsonResponse(filtered_list, safe=False)
            return JsonResponse(data, safe=False)

    except Exception as e:
        print(e)
        return JsonResponse([f'Something went wrong. Could not fetch data [{e}]'], safe=False)

def get_accrediations(request):
    try:
        with open("static/autocomplete_data/accrediations.json", 'r') as f:
            data = json.load(f)

            if request.GET.get('q'):
                accrediation_list = []
                query = request.GET['q']

                _ = [[accrediation_list.append(f'{accrediation} ({full_form})') for accrediation in values] for full_form, values in data.items()]

                filtered_list = list(filter(lambda x: query in x.lower().replace('(', ''), accrediation_list))
                filtered_list.sort()

                return JsonResponse(filtered_list, safe=False)
            return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse([f'Something went wrong. Could not fetch data [{e}]'], safe=False)
