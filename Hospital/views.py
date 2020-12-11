from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from Doctor.models import Doctor
from .filters import DoctorFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.contrib.auth import login, authenticate
from .models import Hospital
from Hospital.forms import HospitalForm, HospitalUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

import django_tables2 as tables

class DoctorTable(tables.Table):
    first_name = tables.Column(attrs={"td": {"class": "red"}})

    class Meta:
        model = Doctor 
        exclude = ['id', 'user','doctor_registeration_no','email','phone_number','experience','affiliation','address','adharcardno']
        # attrs = {"thead": "thead-dark"}

class FilteredDoctorListView(SingleTableMixin, FilterView):
    table_class = DoctorTable
    model = Doctor
    template_name = "Hospital/index2.html"

    filterset_class = DoctorFilter


class HospitalView(TemplateView):
    template_name='HospitalRegisteration.html'
    
    def get(self,request):
        form = HospitalForm()
        form2 = HospitalUserForm()
        return render(request,self.template_name,{'form':form, 'form2': form2})
     
    def post(self,request):
        if request.method == 'POST':
            form =  HospitalUserForm(request.POST)
            form2 = HospitalForm(request.POST)
            if form.is_valid() and form2.is_valid():              

                User = get_user_model()
               
                user = User.objects.create_user(
                    form.data['username'], 
                    form2.data['email'], 
                    form.data['password1'], 
                    first_name=form2.data['name'],
                    is_hospital = True,
                )

                HospitalRegisterationForm=form2.save(commit=False)
                HospitalRegisterationForm.user=user
                HospitalRegisterationForm.save()

                user = authenticate(username=form2.data['username'], password=form2.data['password1'])
                login(request, user)
                return redirect('home')
            else:
                form = HospitalUserForm()
                form2 = HospitalForm()
            return render(request,self.template_name, {'form': form,'form2':form2})