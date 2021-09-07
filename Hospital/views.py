"""View for hospital"""
import json
from datetime import datetime

import django_tables2 as tables
from ARCIT.views import raw_sql_executor
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.http.request import QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from Doctor.models import Doctor
from Patient.models import Appointment, Patient
from Patient.views import get_appointment_token

from .models import Hospital

User = get_user_model()

def AffiliatedDoctors(request):
    template = "Hospital/affiliatedDoctors.html"

    query = f'''
        select 
            da.id as active_hour_id,
            d.user_id as doctor_id,
            d.name,
            d.specialization,
            da.arrival_time,
            da.departure_time
        from Doctor_activehour da
        left join Doctor_doctor d on d.user_id = da.doctor_id
        where 
            affiliation='{User.objects.get(username=request.session['loggedin_username']).username}'
            AND for_hospital=1
            AND strftime('%H:%M:%S',datetime('now','localtime')) BETWEEN TIME(da.arrival_time) and TIME(da.departure_time)
        ORDER BY d.name;
    '''

    doctors = raw_sql_executor(query)
    return render(request, template, { "doctors":doctors })

class HospitalProfileView(TemplateView):
    '''For hospital profile'''
    template_name='Hosptial/profile.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        hospital = Hospital.objects.get(user=user)
        return render(request,self.template_name,{'profile':hospital})

def get_hospitals(request):
    '''Get autocompleted hospitals'''
    filtered_results = list()
    query = request.GET['q']
    hospitals = User.objects.all().filter(is_hospital=True).values_list("username", "first_name")
    filtered_hospitals = hospitals.filter(Q(first_name__contains=query)|Q(username__contains=query))
    _=[filtered_results.append(hospital[0]) for hospital in filtered_hospitals]
    return JsonResponse(filtered_results, safe=False)

def get_hospital_specializations(request):
    try:
        with open("static/autocomplete_data/h_specializations.json", 'r') as f:
            json_data = json.load(f)
            
            if request.GET.get('q'):
                query = request.GET['q']

                specializations = list(filter(lambda specialization: query in specialization.lower(), json_data))
                specializations.sort()
                
                return JsonResponse(specializations, safe=False)
            return JsonResponse(json_data, safe=False)

    except Exception as e:
        return JsonResponse([f'Something went wrong. Could not fetch data [{e}]'], safe=False)

@csrf_exempt
def set_appointment(request):
    form_data = QueryDict(request.POST['data'].encode('ASCII'))

    phone_number = form_data['patient_phone_number'].strip()[-10:]
    doctor_id = form_data['doctor_id']
    active_hour_id = form_data['active_hour_id']
    try:
        patient_id = Patient.objects.get(phone_number=phone_number).id
        appointment_date = datetime.now().date()

        saved_appointments = Appointment.objects.filter(Q(patient_id=patient_id) & Q(doctor_id=int(doctor_id)))

        if saved_appointments.exists() and saved_appointments is not None:
            for appointment in saved_appointments:
                if appointment.doctor_id == int(doctor_id) and appointment.active_hour_id == int(active_hour_id) and appointment.date == appointment_date:
                    return JsonResponse({"error": "Appointment already exists!"}, safe=False)

        token_number = get_appointment_token(doctor_id, active_hour_id, patient_id, appointment_date)
        
        Appointment(
            patient_id = patient_id,
            doctor_id = doctor_id,
            active_hour_id = active_hour_id,
            date = appointment_date,
            token_number = token_number
        ).save()

        return JsonResponse({"success": f"Appointment taken, your token number is: <strong>{token_number}<strong>"}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"error": f"No patient registered with this number."}, status=200)

