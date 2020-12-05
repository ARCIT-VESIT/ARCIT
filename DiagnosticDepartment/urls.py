from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
   # path('', views.Home.as_view(), name='home'),
    path('DiagnosticDepartment/', views.upload, name='upload'), #5.12 min v
    

   # path('admin/', admin.site.urls),
]