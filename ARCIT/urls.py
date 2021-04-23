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
    path('', include ('Doctor.urls')),
    path('', include('Patient.urls')),
    path('', include('DiagnosticDepartment.urls')),
    path('', include('Hospital.urls')),
    url(r'^$', core_views.log_in, name='login'),
    url(r'^signup/$', TemplateView.as_view(template_name='sidebar.html'), name='home'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='Authentication/logout.html'), name='logout'),
    # url(r'^signup/$', core_views.signup, name='signup'),
    # url(r'^home/$', core_views.UserTypeView.as_view(template_name='home1.html'), name='dropdown'),
    # url(r'^home/$', core_views.UserTypeView.as_view(template_name='Authentication/signup.html'), name='dropdown'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
