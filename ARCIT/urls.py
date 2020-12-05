"""ARCIT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from ARCIT import views as core_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('otpAuth.urls')),
    path('',include ('doc_reg.urls')),
    path('', include('patregistration.urls')),
    path('', include('Hospital.urls')),
    
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^home/$', core_views.UserTypeView.as_view(template_name='home1.html'), name='dropdown'),
]
