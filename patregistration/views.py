from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from patregistration.forms import RegForm, PatUserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Patients
from django.contrib.auth import login, authenticate

class docregister(TemplateView):
    template_name='patreg.html'
    
    def get(self,request):
        form = RegForm()
        form2 = PatUserForm()
        
        return render(request,self.template_name,{'form':form, 'form2': form2  } )

    def post(self,request):
        if request.method == 'POST':
            form = PatUserForm(request.POST)
            form2 = RegForm(request.POST)
            if form.is_valid() and form2.is_valid():
                # user=form.save()

                user = User.objects.create_user(
                    form.data['username'], 
                    form2.data['email'], 
                    form.data['password1'], 
                    first_name=form2.data['first_name'],
                    last_name=form2.data['last_name'],
                )

                patform=form2.save(commit=False) 
                patform.user=user
                patform.save()
                # username=form.cleaned_data('username')
                # password=form.cleaned_data('password1')
                
                

                user = authenticate(username=form2.data['username'], password=form2.data['password1'])
                login(request, user)

                #form = RegForm()
                
                
                return redirect('home')
            else:
                form = PatUserForm()
                form2=RegForm()
            return render(request,self.template_name, {'form': form,'form2':form2})
        

