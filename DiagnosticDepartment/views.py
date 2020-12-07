# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate

from .forms import DiagnosticDepartmentForm, DiagnosticDepartmentUserForm, DiagnosticDepartmentSignupForm
#from .models import DiagnosticDe

User = get_user_model()

def upload(request):
    
    form = DiagnosticDepartmentForm()
    context = {}
    context['form'] = form

    if request.method == 'POST':
        form = DiagnosticDepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            data=form.save(commit=True)
            url = data.report.url
            print(url)
            return render(request, 'DiagnosticDepartment.html', {'msg': "file uploaded successfully", 'url':url})

    return render(request, 'DiagnosticDepartment.html', context) 
    #add content after

class DiagnosticLoginView(TemplateView):
    template_name='HospitalRegisteration.html'
    
    def get(self,request):
        
        form = DiagnosticDepartmentSignupForm()
        form2 = DiagnosticDepartmentUserForm()

        return render(request,self.template_name,{'form':form, 'form2': form2})
     
    def post(self,request):
        if request.method == 'POST':
            form =  DiagnosticDepartmentUserForm(request.POST)
            form2 = DiagnosticDepartmentSignupForm(request.POST)

            if form.is_valid() and form2.is_valid():                             
                user = User.objects.create_user(
                    form.data['username'], 
                    form2.data['email'], 
                    form.data['password1'], 
                    first_name=form2.data['name'],
                    is_diagnosticDepartment = True,
                )

                DiagnosticDepartmentForm=form2.save(commit=False)
                DiagnosticDepartmentForm.user=user
                DiagnosticDepartmentForm.save()

                user = authenticate(username=form2.data['username'], password=form2.data['password1'])
                login(request, user)
                return redirect('home')
            else:
                form =  DiagnosticDepartmentUserForm()
                form2 = DiagnosticDepartmentSignupForm()
            return render(request,self.template_name, {'form': form,'form2':form2})