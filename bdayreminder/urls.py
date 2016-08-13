from django.conf.urls import url

from . import views

app_name = "bdayreminder"
urlpatterns = [
    url(r'^patients', views.patients, name='patients'),
    url(r'^api_auth', views.api_auth, name="api_auth"),
    url(r'^revoke', views.revoke, name="revoke_token"),
    url(r'^send_emails', views.send_emails, name="send_emails"),
    url(r'^$', views.index, name='index')

]
