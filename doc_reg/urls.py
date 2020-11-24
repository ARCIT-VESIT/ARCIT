from django.conf.urls import url
from doc_reg.views import Doctor

urlpatterns = [

    url(r'^docreg/$', Doctor.as_view(template_name='doc_reg.html'), name='docreg'),
]
