"""View for hospital"""
import django_tables2 as tables
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from Doctor.models import Doctor

from ARCIT.forms import UserForm
from .forms import HospitalForm

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
        print(user)
        print(hospital)
        return render(request,self.template_name,{'profile':hospital})
