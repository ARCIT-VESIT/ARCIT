"""View for hospital"""
import django_tables2 as tables
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from Doctor.models import Doctor

from Hospital.forms import HospitalForm, HospitalUserForm

from .filters import DoctorFilter
from .models import Hospital

User = get_user_model()

class DoctorTable(tables.Table):
    '''to view all doctors as table'''
    first_name = tables.Column(attrs={"td": {"class": "red"}})

    class Meta:
        '''Meta info about doctor table'''
        model = Doctor
        exclude = ['id',
                    'user',
                    'doctor_registeration_no',
                    'email',
                    'phone_number',
                    'experience',
                    'affiliation',
                    'address',
                    'adharcardno']
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

class HospitalView(TemplateView):
    '''Registeration for hospital'''
    template_name='Hospital/registeration.html'

    def get(self, request, *args, **kwargs):
        form = HospitalForm()
        form2 = HospitalUserForm()
        return render(request,self.template_name,{'form':form, 'form2': form2})

    def post(self,request):
        '''request to handle registeration of hospital form'''
        if request.method == 'POST':
            form =  HospitalUserForm(request.POST)
            form2 = HospitalForm(request.POST)
            if form.is_valid() and form2.is_valid():

                user = User.objects.create_user(
                    form.data['username'],
                    form2.data['email'],
                    form.data['password1'],
                    first_name=form2.data['name'],
                    is_hospital = True,
                )

                hospital_registeration_form=form2.save(commit=False)
                hospital_registeration_form.user=user
                hospital_registeration_form.save()

                user= authenticate(username=form2.data['username'],password=form2.data['password1'])
                login(request, user)
                return redirect('login')
            else:
                form = HospitalUserForm()
                form2 = HospitalForm()
            return render(request,self.template_name, {'form': form,'form2':form2})
        return None


class HospitalProfileView(TemplateView):
    '''For hospital profile'''
    template_name='Hosptial/profile.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.session['loggedin_username'])
        hospital = Hospital.objects.get(user=user)
        print(user)
        print(hospital)
        return render(request,self.template_name,{'profile':hospital})
