"""View for hospital"""
import json
import django_tables2 as tables
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Q

from Doctor.models import Doctor

from .filters import DoctorFilter
from .models import Hospital

User = get_user_model()

class DoctorTable(tables.Table):
    '''to view all doctors as table'''
    first_name = tables.Column(attrs={"td": {"class": "red"}})

    class Meta:
        '''Meta info about doctor table'''
        model = Doctor
        fields = ['name', 'specialization', ]
        # attrs = {"thead": "thead-dark"}

# class FilteredDoctorListView(SingleTableMixin, FilterView):
#     table_class = DoctorTable
#     model = Doctor
#     template_name = "Hospital/affiliatedDoctors.html"

#     filterset_class = DoctorFilter

class FilteredDoctorListView(TemplateView):
    '''For hospitals to get all the affiliated doctors'''
    template_name = "Hospital/affiliatedDoctors.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        doctor_list = Doctor.objects.filter(affiliation = user)
        doctor_filter = DoctorFilter(request.GET, queryset=doctor_list)
        return render(request,self.template_name,{'filter':doctor_filter})

    def post(self, request):
        '''method to handle filter request'''
        return render(request,self.template_name)

class HospitalProfileView(TemplateView):
    '''For hospital profile'''
    template_name='Hosptial/profile.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        hospital = Hospital.objects.get(user=user)
        return render(request,self.template_name,{'profile':hospital})

def get_hospitals(request):
    '''Get autocompleted hospitals'''
    # filtered_results = list()
    # query = request.GET['q']
    # hospitals = User.objects.all().filter(is_hospital=True).values_list("username", "first_name")
    # filtered_hospitals = hospitals.filter(Q(first_name__contains=query)|Q(username__contains=query))
    # _=[filtered_results.append(f'{hospital[1]} ({hospital[0]})') for hospital in filtered_hospitals]
    # return JsonResponse(filtered_results, safe=False)
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
