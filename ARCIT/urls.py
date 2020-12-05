from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from ARCIT import views as core_views
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('otpAuth.urls')),
    path('',include ('doc_reg.urls')),
    path('', include('patregistration.urls')),
    path('', include('PatientHistory.urls')),
    path('', include('DiagnosticDepartment.urls')),
    path('', include('Hospital.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^home/$', core_views.UserTypeView.as_view(template_name='home1.html'), name='dropdown'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
