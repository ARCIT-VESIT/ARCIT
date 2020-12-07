from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from doc_reg.forms import DoctorForm, DoctorUserForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Doctor
from patregistration.models import Patients

class DoctorView(TemplateView):
    template_name='doc_reg.html'
    
    def get(self,request):
        form = DoctorForm()
        form2 = DoctorUserForm()
        return render(request,self.template_name,{'form':form, 'form2': form2})
     
    def post(self,request):
        if request.method == 'POST':
            form =  DoctorUserForm(request.POST)
            form2 = DoctorForm(request.POST)
            if form.is_valid() and form2.is_valid():              

                User = get_user_model()

                user = User.objects.create_user(
                    form.data['username'], 
                    form2.data['email'], 
                    form.data['password1'], 
                    first_name=form2.data['first_name'],
                    last_name=form2.data['last_name'],
                    is_doctor = True,
                )
                patform=form2.save(commit=False) 
                patform.user=user
                patform.save()

                user = authenticate(username=form2.data['username'], password=form2.data['password1'])
                login(request, user)
                return redirect('home')
            else:
                form = DoctorUserForm()
                form2=DoctorForm()
            return render(request,self.template_name, {'form': form,'form2':form2})