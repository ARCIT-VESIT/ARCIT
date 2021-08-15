# from datetime import date, datetime
"""View for patient"""
import json

import requests
from ARCIT.views import raw_sql_executor
from django.contrib.auth import get_user_model
from django.db import connection
from django.http.response import JsonResponse
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import PatientHistoryForm
from .models import Patient

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
    return render(request, 'Patient/dashboard.html', {})
