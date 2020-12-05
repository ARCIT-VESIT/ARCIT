from django.conf.urls import url
from doc_reg.views import DoctorView

urlpatterns = [

    url(r'^docreg/$', DoctorView.as_view(template_name='doc_reg.html'), name='docreg'),
]
