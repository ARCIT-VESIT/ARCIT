# from datetime import date, datetime
"""View for patient"""
import json
from datetime import datetime

import requests
from ARCIT.views import raw_sql_executor
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.models.query_utils import Q
from django.http import QueryDict
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from Doctor.models import Doctor

from .forms import PatientHistoryForm
from .models import Appointment, Patient

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
        return render(request,
                    'Doctor/addPatientHistory.html',
                    {'msg': "file uploaded successfully", 'url':url})

    return render(request, 'Doctor/addPatientHistory.html', context)

class ViewPatientProfile(TemplateView):
    '''view for patient to view their profile'''
    template_name='Patient/profile.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        patient = Patient.objects.get(user=user)
        # today = date.today()
        # age = today.year - datetime.year(patient.dob) - ((today.month, today.day)
        #       < (datetime.month(patient.dob), datetime.day(patient.dob)))
        # age = patient.dob
        return render(request,self.template_name,{'profile':patient})

class MapColumnHeadings():
    def __init__(self, cursor):
        self._cursor = cursor
    
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()

        return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }

class ViewPatientHistory(TemplateView):
    '''For patient to view their history'''

    def raw_sql_executor(self, request, user):
        rows = []

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    select
                        dd_user.first_name || ' (' || dd_user.Username || ')' as handled_by,
                        p_user.first_name || ' (' || p_user.Username || ')' as referred_from,
                        ph.id,
                        CASE
                            WHEN medical_status = '1' THEN 'Normal'
                            WHEN medical_status = '2' THEN 'Mild'
                            WHEN medical_status = '3' THEN 'Critical'
                            ELSE 'None'
                        END AS medical_status,
                        symtomps,
                        disease,
                        affected_area,
                        timespan, course_duration,
                        follow_up,
                        referred_from_id,
                        referred_to,
                        ph.user_id,
                        ph.created_on,
                        prescription,
                        ddr.name, ddr.supervisor,
                        ddr.referred_by,
                        ddr.handled_by_id,
                        ddr.report,
                        ddr.user_id,
                        ddr.created_on as ddr_created_on,
                        ddr.patient_history_id,
                        ddr.id as ddr_id
                    from "Patient_patienthistory" ph
                    left join "DiagnosticDepartment_diagnosticdepartmentreport" ddr
                        on ddr.patient_history_id = ph.id
                    left join "ARCIT_user" dd_user
                        on dd_user.id = ddr.handled_by_id
                    left join "ARCIT_user" p_user
                        on p_user.id = ph.referred_from_id
                    where ph.user_id = %s
                    order by ph.created_on desc""", [user.id]
                )

                for row in MapColumnHeadings(cursor):

                    row['downloadLink'] = f'{request.build_absolute_uri("/media/")}{row["report"]}'
                    rows.append(row)
        except:
            pass

        return rows

    def get(self,request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username']) if request.session.has_key('is_patient') else Patient.objects.get(phone_number=request.session['phoneNumber']).user
        model = self.raw_sql_executor(request, user)

        return render(request,self.template_name,{'models':model})

def get_states(request):
    try:
        with open("static/autocomplete_data/states.json", 'r') as f:
            json_data = json.load(f)
            
            if request.GET.get('q'):
                query = request.GET['q']

                states = list(filter(lambda state: query in state.lower(), json_data))
                states.sort()
                
                return JsonResponse(states, safe=False)
            return JsonResponse(json_data, safe=False)

    except Exception as e:
        return JsonResponse([f'Something went wrong. Could not fetch data [{e}]'], safe=False)

def get_news(request):
    state = Patient.objects.get(user=User.objects.get(username=request.session['loggedin_username']).id).state
    newsUrl = f'https://newsapi.org/v2/top-headlines?country=in&category=health&q={state}&apiKey=134ea850951345ff90773d8a6cb4ce4b'
    response = requests.get(newsUrl, params=request.GET)

    if response.status_code == 200:
        news_data = json.loads(response.content)
        return render(request, 'Patient/news.html', {'trending_news': news_data['articles'] })

def most_visited_specialities(request):
    labels = []
    data = []
    
    query = '''
        SELECT d.specialization, count(*) AS visit_frequency from "Patient_patienthistory" ph
            LEFT JOIN "Doctor_doctor" d ON d.user_id = ph.referred_from_id
            WHERE ph.user_id = %s
        GROUP BY d.specialization
        ORDER BY visit_frequency DESC
        LIMIT 5;
    '''

    dataset = raw_sql_executor(query, [User.objects.get(username=request.session['loggedin_username']).id])
    
    for record in dataset:
        labels.append(record['specialization'])
        data.append(record['visit_frequency'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def frequent_diseases(request):
    labels = []
    data = []
    
    query = '''
        SELECT ph.disease, count(*) AS disease_frequency FROM "Patient_patienthistory" ph
            LEFT JOIN "Patient_patient" p ON p.user_id = ph.user_id
            WHERE ph.user_id = %s
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

def dashboard(request):
    return render(request, 'Patient/dashboard.html', {"appointment_count": len(upcoming_appointments_query(request))})

def doctor_appointment(request):
    template = 'Patient/setAppointment.html'
    if 'filterText' in request.GET:
        try:
            pincode = Patient.objects.get(user=User.objects.get(username=request.session['loggedin_username'])).pincode
            filter_text = request.GET['filterText']

            query = f'''
                SELECT 
                    user_id,
                    name,
                    experience,
                    affiliation,
                    specialization,
                    accreditation,
                    address,
                    pincode,
                    ah.active_hours
                FROM "Doctor_doctor" d
                left join (
                    select 
                        doctor_id,
                        group_concat(json_object(
                            'id', id, 
                            'arrival_time', arrival_time, 
                            'departure_time', departure_time, 
                            'doctor_id', doctor_id, 
                            'for_hospital', for_hospital)) 
                        as active_hours
                    from "Doctor_activehour" where id in (
                        WITH split(one, many, str) AS (
                            SELECT active_hours, '', active_hours||','
                                FROM "Doctor_doctor"
                            UNION ALL SELECT one,
                                substr(str, 0, instr(str, ',')),
                                substr(str, instr(str, ',')+1)
                            FROM "split" WHERE str !=''
                        ) SELECT REPLACE(REPLACE(trim(many),'[',''), ']', '')
                                FROM "split"
                                WHERE many!='' 
                            ORDER BY many
                    )
                    GROUP BY doctor_id
                ) ah on ah.doctor_id = d.user_id
                WHERE 
                    name like '%{filter_text}%' or
                    specialization like '%{filter_text}%' or
                    accreditation like '%{filter_text}%' or
                    pincode = {pincode}
                ORDER BY(
                    CASE
                    WHEN name like '%{filter_text}%' THEN 1
                    WHEN specialization like '%{filter_text}%' THEN 2
                    WHEN accreditation like '%{filter_text}%' THEN 3
                    ELSE 4
                END);
            '''

            doctors= raw_sql_executor(query)

            for doctor in doctors:
                if doctor["active_hours"] is not None:
                    active_hours_tuple = eval(doctor["active_hours"])
                    active_hours = []

                    if type(active_hours_tuple) is tuple:
                        for active_hour_tuple in active_hours_tuple:
                            get_active_hour_as_model(active_hour_tuple, active_hours)
                    else:
                        get_active_hour_as_model(active_hours_tuple, active_hours)
                        
                    doctor["active_hours"] = dict
                    doctor["active_hours"] = active_hours

            return render(request,template,{"doctors":doctors, 'filterText': filter_text})
        except Exception as ex:
            return render(request,template,{'doctors':doctors})
    return render(request, template)

def get_active_hour_as_model(tuple, active_hours):
    active_hours.append({
        'id' : tuple['id'],
        'arrival_time' : tuple['arrival_time'],
        'departure_time' : tuple['departure_time'],
        'doctor_id' : tuple['doctor_id'],
        'for_hospital' : tuple['for_hospital']
    })

def get_appointment_token(doctor_id, active_hour_id, patient_id, appointment_date):
    saved_appointments = Appointment.objects.filter(Q(doctor_id=Doctor.objects.get(user=doctor_id).user.id) & Q(active_hour_id=active_hour_id)).order_by('-token_number')

    if saved_appointments.exists() and saved_appointments is not None:
        for appointment in saved_appointments:
            if appointment.doctor_id == int(doctor_id) and appointment.active_hour_id == int(active_hour_id) and appointment.date == appointment_date:
                return 1 if appointment.patient_id == patient_id else appointment.token_number + 1
    return 1

@csrf_exempt
def set_appointment(request):
    form_data = QueryDict(request.POST['data'].encode('ASCII'))

    doctor_id = form_data['doctor_id']
    active_hour_id = form_data['active_hour_id']
    patient_id = Patient.objects.get(user=User.objects.get(username=request.session['loggedin_username'])).id
    appointment_date = datetime.strptime(f"{form_data['appointment_date'].replace('-', '/', 2)[2:]}", '%y/%m/%d').date()

    saved_appointments = Appointment.objects.filter(Q(patient_id=patient_id) & Q(doctor_id=int(doctor_id)))

    if saved_appointments.exists() and saved_appointments is not None:
        for appointment in saved_appointments:
            if appointment.doctor_id == int(doctor_id) and appointment.active_hour_id == int(active_hour_id) and appointment.date == appointment_date:
                return JsonResponse({"error": "Appointment already exists for the selected date and time"}, safe=False)

    token_number = get_appointment_token(doctor_id, active_hour_id, patient_id, appointment_date)

    Appointment(
        patient_id = patient_id,
        doctor_id = doctor_id,
        active_hour_id = active_hour_id,
        date = appointment_date,
        token_number = token_number
    ).save()

    return JsonResponse({"success": f"Appointment taken, your token number is: <strong>{token_number}<strong>"}, status=200)

def upcomingAppointments(request):
    return render(request, "Patient/appointments.html", {"appointments": upcoming_appointments_query(request)})

def upcoming_appointments_query(request):
    query = '''
        SELECT 
            pa.id,
            d.name as doctor_name,
            pa.token_number,
            da.arrival_time,
            da.departure_time,
            pa.date,
            da.for_hospital,
            d.affiliation,
            d.accreditation,
            d.specialization,
            d.address
        from "Patient_appointment" pa
            left join "Doctor_activehour" da on da.id = pa.active_hour_id
            left join "Doctor_doctor" d on d.user_id = pa.doctor_id
        WHERE 
            DATETIME(DATE(pa.date) || ' ' || TIME(da.departure_time)) >= datetime('now','localtime') and 
            patient_id = %s
        ORDER BY
            pa.date,
            da.arrival_time
    '''
    dataset = raw_sql_executor(query, [Patient.objects.get(user=User.objects.get(username=request.session['loggedin_username']).id).id])
    return dataset
