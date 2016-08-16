from django.conf.urls import url

from . import views

app_name = "medications"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^patient_detail/', views.patient_detail, name='patient_detail'),
    url(r'^patients', views.patients, name='patients'),
    url(r'^authorize', views.authorize, name="authorize"),
]
