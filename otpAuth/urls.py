from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.urls import path
from . import views
from otpAuth.views import OtpAuthView, VerifyOtpView

urlpatterns = [
    # path('otpAuth/', views.index, name='otpIndex'),
    url(r'^otpAuth/$', OtpAuthView.as_view(template_name='otpAuthIndex.html'), name='otpIndex'),
    url(r'^otpAuth/verifyOtp$', VerifyOtpView.as_view(template_name='enterOtp.html'), name='enterOtp'),
]