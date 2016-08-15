from django.conf.urls import url

from . import views

app_name = "bdayreminder"
urlpatterns = [
    url(r'^patients', views.patients, name='patients'),
    url(r'^login', views.login, name="login"),
    url(r'^revoke', views.revoke, name="revoke_token"),
    url(r'^send_emails', views.send_emails, name="send_emails"),
    url(r'^send_texts', views.send_texts, name="send_texts"),
    url(r'^$', views.index, name='index')

]
