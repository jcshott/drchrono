from django.conf.urls import url

from . import views

app_name = "medications"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^process_refill/', views.process_refill, name='process_refill'),
    url(r'^process_renewal/', views.process_renewal, name='process_renewal'),
    url(r'^patients', views.patients, name='patients'),
    url(r'^authorize', views.authorize, name="authorize"),
    url(r'^test_api', views.test_api, name="test_api"),
]
