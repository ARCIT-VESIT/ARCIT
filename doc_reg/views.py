from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.views.generic import TemplateView
from doc_reg.forms import DoctorForm, DoctorUserForm
from django.contrib.auth.models import User

class Doctor(TemplateView):
    template_name='doc_reg.html'
    
    def get(self,request):
        form = DoctorForm()
        form2 = DoctorUserForm()
        return render(request,self.template_name,{'form':form, 'form2': form2})
    
    def post(self,request):
        if request.method == 'POST':
            form = DoctorForm(request.POST)
            form2 = DoctorUserForm(request.POST)
            if form.is_valid():              
                form.save()

                new_user = User.objects.create_user(
                    form2.data['username'], 
                    form.data['email'], 
                    form2.data['password1'], 
                    first_name=form.data['first_name'],
                    last_name=form.data['last_name'],
                )

                form = Doctor()
                user = authenticate(username=form2.data['username'], password=form2.data['password1'])
                login(request, user)
                return redirect('home')
            else:
                form = DoctorForm()
                return render(request,self.template_name, {'form': form})