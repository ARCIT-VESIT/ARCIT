"""View for Doctor"""
import hashlib
import json
from random import randint

from ARCIT.views import raw_sql_executor
from django.contrib.auth import get_user_model
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from Patient.forms import PatientHistoryForm
from Patient.models import Patient, PatientHistory

from .models import ActiveHour, Doctor

User = get_user_model()

class ViewDoctorProfile(TemplateView):
    '''View for doctor profile'''
    template_name='Doctor/profile.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        doctor = Doctor.objects.get(user=user)

        query = '''
            select * from "Doctor_activehour" where id in(
                WITH split(one, many, str) AS (
                    SELECT  active_hours, '', active_hours||','
                        FROM "Doctor_doctor"
                        where id = %s
                    UNION ALL SELECT one,
                        substr(str, 0, instr(str, ',')),
                        substr(str, instr(str, ',')+1)
                    FROM "split" WHERE str !=''
                ) SELECT REPLACE(REPLACE(trim(many),'[',''), ']', '')
                        FROM "split"
                        WHERE many!='' 
                    ORDER BY many)
        '''
        
        dataset = raw_sql_executor(query, [doctor.id])

        if len(dataset) > 0 and 'error' in dataset:
            query = '''
                select * from "Doctor_activehour"
                where Id IN (
                    select 
                        jsonb_array_elements(active_hours)::bigint as Id 
                    from "Doctor_doctor" 
                    where id = %s
                );
            '''

            dataset = raw_sql_executor(query, [doctor.id])

        # today = date.today()
        # age = today.year - datetime.year(patient.dob) - ((today.month, today.day)
        #       < (datetime.month(patient.dob), datetime.day(patient.dob)))
        # age = patient.dob
        return render(request,self.template_name,{'profile':doctor, 'active_hours': dataset})

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

def is_chain_valid(request):
    user = Patient.objects.get(phone_number=request.session['phoneNumber']).user
    patients = PatientHistory.objects.filter(user=user.id)
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

def mine_patient_history(form_data, request):
    user = Patient.objects.get(phone_number=request.session['phoneNumber']).user
    patients = PatientHistory.objects.filter(user=user.id)
    patient_count = patients.count()

    if patient_count == 0:
        random_number = randint(56543, 95715)
        form_data.nonce = random_number
        form_data.previous_hash = hashlib.sha256(str(random_number).encode()).hexdigest()
        # return { form2.nonce, form2.previous_hash }
    else:
        previous_block = patients.last()
        previous_nonce = previous_block.nonce
        nonce = proof_of_work(previous_nonce)
        previous_hash = hash_block(previous_block)
        form_data.nonce = nonce
        form_data.previous_hash = previous_hash

class AddPatientDataView(TemplateView):
    '''For doctors to add new patient'''
    template_name='Doctor/addPatientHistory.html'

    def get(self,request, *args, **kwargs):
        form = PatientHistoryForm()
        # res = is_chain_valid(request)

        return render(request,self.template_name,{'form':form})

    def post(self,request):
        '''Post method to add patient history'''
        form=PatientHistoryForm(request.POST)

        user = Patient.objects.get(phone_number=request.session['phoneNumber']).user
        doctor_user = User.objects.get(username=request.session['loggedin_username'])

        if form.is_valid():
            formdata = form.save(commit=False)
            mine_patient_history(formdata, request)
            formdata.user=user
            formdata.referred_from = doctor_user
            formdata.save()

            # return render(request, 'Doctor/index.html')
            return redirect('viewHistory')
        form = PatientHistoryForm()
        return render(request,self.template_name, {'form': form})

def get_specializations(request):
    try:
        with open("static/autocomplete_data/specializations.json", 'r') as f:
            json_data = json.load(f)
            
            if request.GET.get('q'):
                query = request.GET['q']

                specializations = list(filter(lambda specialization: query in specialization.lower(), json_data))
                specializations.sort()
                
                return JsonResponse(specializations, safe=False)
            return JsonResponse(json_data, safe=False)

    except Exception as e:
        return JsonResponse([f'Something went wrong. Could not fetch data [{e}]'], safe=False)

def get_accreditations(request):
    try:
        with open("static/autocomplete_data/accreditations.json", 'r') as f:
            json_data = json.load(f)

            if request.GET.get('q'):
                accreditations = []
                query = request.GET['q']

                _ = [[accreditations.append(f'{accreditation} ({full_form})') for accreditation in short_form] for full_form, short_form in json_data.items()]

                filtered_accreditations = list(filter(lambda accreditation: query in accreditation.lower().replace('(', ''), accreditations))
                filtered_accreditations.sort()

                return JsonResponse(filtered_accreditations, safe=False)
            return JsonResponse(json_data, safe=False)

    except Exception as e:
        return JsonResponse([f'Something went wrong. Could not fetch data [{e}]'], safe=False)

def dashboard_data(request):
    labels = []
    data = []

    query = '''
        SELECT 
            disease, 
            count(*) AS disease_frequency 
            from "Patient_patienthistory" ph
            left join "Doctor_doctor" d on d.user_id = ph.referred_from_id
        WHERE d.user_id = %s
            GROUP BY ph.disease
            ORDER BY disease_frequency
        LIMIT 10;
    '''
    
    dataset = raw_sql_executor(query, [User.objects.get(username=request.session['loggedin_username']).id])
    
    for record in dataset:
        labels.append(record['disease'])
        data.append(record['disease_frequency'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def patient_treated(request):
    data = PatientHistory.objects.filter(referred_from=User.objects.get(username=request.session['loggedin_username']).id).count
    return JsonResponse(data, safe=False)

def dashboard(request):
    userid = User.objects.get(username=request.session['loggedin_username']).id
    cases_handled = PatientHistory.objects.filter(referred_from=userid).count
    years_practicing = Doctor.objects.get(user=userid).experience

    return render(request, 'Doctor/dashboard.html', {'cases_handled': cases_handled, 'experience': years_practicing})

def set_active_hour(request):
    form_data = request.POST
    active_hour_id = form_data['active_hour']
    is_for_hospital = False
    try:
        if form_data['for_hospital'] == 'on':
            is_for_hospital = True
    except:
        pass

    if active_hour_id == '':
        user = User.objects.get(id=form_data['doctor_id'])
        doctor = Doctor.objects.get(user=user)

        active_hour_model = ActiveHour()
        active_hour_model.user = user
        active_hour_model.arrival_time = form_data['start_time']
        active_hour_model.departure_time = form_data['departure_time']
        active_hour_model.doctor_id = form_data['doctor_id']
        active_hour_model.for_hospital = is_for_hospital
        active_hour_model.save()

        doctor.active_hours.append(active_hour_model.id)

        doctor.save()
    else:
        ActiveHour.objects.filter(id=int(active_hour_id)).update(
            arrival_time=form_data['start_time'],
            departure_time=form_data['departure_time'],
            for_hospital=is_for_hospital
        )
    return redirect('doctorprofile')

def delete_active_hour(request):
    id = int(request.POST['active_hour'])
    user = request.session['loggedin_username']
    
    ActiveHour.objects.get(id=id).delete()
    active_hours = Doctor.objects.get(user_id=User.objects.get(username=user).id).active_hours
    active_hours.remove(id)
    Doctor.objects.filter(user_id=User.objects.get(username=user).id).update(active_hours=active_hours)

    return redirect('doctorprofile')
