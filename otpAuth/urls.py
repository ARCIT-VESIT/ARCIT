from django.conf.urls import url
from .views import OtpAuthView

urlpatterns = [
    url(r'^otpAuth/$', OtpAuthView.as_view(template_name='otpAuthentication.html'), name='otpAuth'),
]
