# Create your views here.
import json
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.http import JsonResponse

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

    def post(self, request, *args, **kwargs):
        
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
                form_data.patient_history_id = kwargs.pop('id')
                form_data.handled_by=dd_user
                form_data.save()
                
                return redirect('viewpatienthistory')

        return render(request, 'DiagnosticDepartment/UploadReport.html', context)

class ViewDiagnosticDepartment(TemplateView):
    template_name='DiagnosticDepartment/profile.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        diagnosticdepartment = DiagnosticDepartment.objects.get(user=user)

        return render (request,self.template_name,{'profile':diagnosticdepartment})

def get_report_types(request):
    try:
        with open("static/autocomplete_data/report_types.json", 'r') as f:
            json_data = json.load(f)

            if request.GET.get('q') or request.GET.get('q') is '':
                report_types = []
                query = request.GET['q']

                if request.session.has_key("is_dd"):
                    _ = [[report_types.append(report_type.capitalize()) for report_type in values] for _, values in json_data.items()]
                else:
                    _ = [report_types.append(keys.capitalize()) for keys, _ in json_data.items()]

                filtered_report_types = list(filter(lambda report_type: query in report_type.lower(), report_types))
                filtered_report_types.sort()

                return JsonResponse(filtered_report_types, safe=False)
            return JsonResponse(json_data, safe=False)

    except Exception as e:
        return JsonResponse([f'Something went wrong. Could not fetch data [{e}]'], safe=False)
