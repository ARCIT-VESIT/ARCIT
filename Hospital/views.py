from django.shortcuts import render
from django.views.generic import TemplateView
from doc_reg.models import Doctor
from .filters import DoctorFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

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


# class IndexView(TemplateView):
#     template_name = "Hospital/index.html"

#     def get(self, request):
#         print('ran')
#         queryset = Doctor.objects.all()

#         # qs = queryset.all()
#         table = DoctorTable(queryset)
        
#         docFilter = DoctorFilter(request.GET, queryset = queryset)
#         queryset = docFilter.qs

#         args = {'doctors': table, 'filter' : docFilter }
#         return render(request, self.template_name, args)

# def resp(request):
#     print('ran')
#     queryset = Doctor.objects.all()

#     # qs = queryset.all()
#     table = DoctorTable(queryset)
    
#     docFilter = DoctorFilter(request.GET, queryset = queryset)
#     queryset = docFilter.qs

#     args = {'doctors': table, 'filter' : docFilter }
#     return render(request, "Hospital/index.html", args)
