from django.shortcuts import render
from django.views.generic import TemplateView
from patregistration.forms import RegForm

class docregister(TemplateView):
    template_name='patreg.html'
    
    def get(self,request):
        form = RegForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        if request.method == 'POST':
            form = RegForm(request.POST)
            if form.is_valid():
                form.save()
            
                form = RegForm()
            
        return render(request,self.template_name,{'form':form})   

# Create your views here.
