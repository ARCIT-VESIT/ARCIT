# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage


from .forms import DiagnosticDepartmentForm
#from .models import DiagnosticDe

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

    return render(request, 'DiagnosticDepartment.html', context) #add content after

# def DiagnosticDepartment(request):
#     if request.method == 'POST':
#         form = DiagnosticDepartmentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('DiagnosticDepartmentList')
#     else:
#         form = DiagnosticDepartmentForm()
#     return render(request, 'DiagnosticDepartment.html'), {
#         'form': form 
#         }
