from django.conf.urls import url

from . import views

app_name = "medications"
urlpatterns = [
    url(r'^patients', views.patients, name='patients'),
    url(r'^authorize', views.authorize, name="authorize"),
    url(r'^$', views.index, name='index')

]
