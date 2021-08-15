from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView, TemplateView

from ARCIT import views as core_views

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ('Doctor.urls')),
    path('', include('Patient.urls')),
    path('', include('DiagnosticDepartment.urls')),
    path('', include('Hospital.urls')),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
    path('register/<str:role>', core_views.RegisterationView.as_view(template_name='sidebar.html'), name='registeration'),
    url(r'^$', core_views.log_in, name='login'),
    url(r'^signup/$', TemplateView.as_view(template_name='sidebar.html'), name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='Authentication/logout.html'), name='logout'),
    url(r'^error/$', TemplateView.as_view(template_name='errorPage.html'), name='error'),
    url(r'^otpAuth/$', core_views.OtpAuth.as_view(template_name='Authentication/otp.html'), name='otpAuth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
