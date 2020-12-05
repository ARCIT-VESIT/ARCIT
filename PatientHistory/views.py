#from django.shortcuts import render

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


from django.views.generic import TemplateView
from PatientHistory.forms import PatientHistori
#from django.contrib.auth.models import User

class PatientHistore(TemplateView):
    template_name='PatientHistory.html'
    
    def get(self,request):
        form = PatientHistori()
        
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form=PatientHistori(request.POST)
        if request.method == 'POST':
            #form = PatientHistori(request.POST)
            if form.is_valid():              
                form.save()

                return redirect('home')
            else:
                form = PatientHistori()
                return render(request,self.template_name, {'form': form})