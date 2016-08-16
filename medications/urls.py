from django.conf.urls import url

from . import views

app_name = "medications"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/patients', views.patients, name='patients'),
    url(r'^(?P<patient_id>[0-9]+)/patients/$', views.patient_detail, name='patient_detail'),
    url(r'^/authorize', views.authorize, name="authorize"),
]
