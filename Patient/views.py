# from datetime import date, datetime
"""View for patient"""
from django.db import connection
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

class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor
    
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()

        return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }

class ViewPatientHistory(TemplateView):
    '''For patient to view their history'''
    template_name='Patient/viewHistory.html'

    def my_custom_sql(self, request, user):
        rows = []

        with connection.cursor() as cursor:
            cursor.execute("""select 
                                    dd_user.first_name || ' (' || dd_user.Username || ')' as handled_by,
                                    p_user.first_name || ' (' || p_user.Username || ')' as referred_from,
                                    ph.id,
                                    medical_status,
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
                                from Patient_patienthistory ph 
                                left join DiagnosticDepartment_diagnosticdepartmentreport ddr 
                                    on ddr.patient_history_id = ph.id 
                                left join ARCIT_user dd_user
                                    on dd_user.id = ddr.handled_by_id
                                left join ARCIT_user p_user
                                    on p_user.id = ph.referred_from_id
                                where ph.user_id = %s""", [user.id])
            
            for row in CursorByName(cursor):

                row['downloadLink'] = f'{request.build_absolute_uri("/media/")}{row["report"]}'
                rows.append(row)

        return rows

    def get(self,request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        model = self.my_custom_sql(request, user)

        return render(request,self.template_name,{'models':model})

class ViewPatientReports(TemplateView):
    '''For patient to view their reports'''
    template_name='Patient/viewReports_p.html'

    def get(self,request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        model = DiagnosticDepartmentReport.objects.filter(user=user).order_by("-created_on")

        return render(request,self.template_name,{'models':model})
