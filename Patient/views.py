# from datetime import date, datetime
"""View for patient"""
import hashlib
import json

from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.core import serializers

from DiagnosticDepartment.models import DiagnosticDepartmentReport
from .forms import PatientHistoryForm, PatUserForm, RegForm
from .models import PatientHistory, Patient

User = get_user_model()

def upload(request):
    '''Method to upload patient history data'''
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

def proof_of_work(previous_nonce):
    new_nonce = 1
    check_nonce = False
    while check_nonce is False:
        hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
        if hash_operation[:4] == '0000':
            check_nonce = True
        else:
            new_nonce += 1
    return new_nonce

hash_block = lambda block : hashlib.sha256(json.dumps(serializers.serialize('json', [ block, ]) , sort_keys = True).encode()).hexdigest()

def is_chain_valid():
    patients = Patient.objects.all()
    previous_block = patients[0]
    block_index = 1
    while block_index < len(patients):
        block = patients[block_index]
        if block.previous_hash != hash_block(previous_block):
            return False
        previous_nonce = previous_block.nonce
        nonce = block.nonce
        hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
        if hash_operation[:4] != '0000':
            return False
        previous_block = block
        block_index += 1
    return True

# def replace_chain(): #New
#     longest_chain = None
#     chain = Patient.objects.all()
#     max_length = len(chain)
#     # for node in network:
#     # response = requests.get(f'http://http://127.0.0.1:8000/get_chain')
#     # if response.status_code == 200:
#     length = chain.count()
#     if length > max_length and is_chain_valid():
#         max_length = length
#         longest_chain = chain
#     if longest_chain:
#         chain = longest_chain
#         return True
#     return False

def minePatient(request, patform):
    patient_count = Patient.objects.count()

    if patient_count is 0:
        patform.nonce = 1
        patform.previous_hash = '0'
        # return { form2.nonce, form2.previous_hash }
    else:
        patients = Patient.objects.all()
        previous_block = patients.last()
        previous_nonce = previous_block.nonce
        nonce = proof_of_work(previous_nonce)
        previous_hash = hash_block(previous_block)
        patform.nonce = nonce
        patform.previous_hash = previous_hash

class PatientRegisterationView(TemplateView):
    '''view for doctor to add a new patient'''
    template_name='Patient/registeration.html'

    def get(self, request, *args, **kwargs):
        # res = is_chain_valid()
        # r2 = replace_chain()
        form = RegForm()
        form2 = PatUserForm()

        return render(request,self.template_name,{'form':form, 'form2': form2  } )

    def post(self,request):
        '''method to handle patient registeration form data'''
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
                minePatient(request, patform)                
                patform.created_by = User.objects.get(username=request.session['loggedin_username'])
                patform.user=user
                patform.save()

                #user=authenticate(username=form2.data['username'],password=form2.data['password1'])
                # login(request, user)
                if User.is_doctor:
                    return redirect('otpIndex')
                else:
                    return redirect('login')
            else:
                form = PatUserForm()
                form2=RegForm()
            return render(request,self.template_name, {'form': form,'form2':form2})
        return None

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
