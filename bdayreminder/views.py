from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail


import api, utils
import os, datetime, requests
from models import Doctor


def index(request):
    # show either the authorize app page or doc's page
    user = request.session.get("user", None)
    if user:
        return redirect("/patients")

    else:
        params = {"redirect": "http%3A//127.0.0.1%3A8000/api_auth",
                "client_id": os.environ["DRCHRONO_CLIENT_ID"]}

        return render(request, "bdayreminder/index.html", params)

def api_auth(request):
    # redirect with the authorization codes from drchrono
    #TODO: error handling if not authorized

    code = request.GET.get("code", "")
    tokens = api.get_tokens(code)

    # Save info in database associated with doctor
    doc = Doctor(access_token = tokens['access_token'],
    refresh_token = tokens['refresh_token'],
    expiration = timezone.now() + datetime.timedelta(seconds=tokens['expires_in']))

    doc.save()
    request.session['user'] = doc.id
    # redirect
    return redirect("/patients")

def patients(request):
    # get data for bday messages
    user_id = request.session['user']

    # birthdays_today = utils.patients_with_bdays(user_id)

    fake = api.get_patients(Doctor.objects.get(pk=user_id))
    # return HttpResponse(birthdays_today)
    # return render(request, "bdayreminder/patients.html", {"patients": birthdays_today})
    return render(request, "bdayreminder/patients.html", {"patients": fake})

def send_emails(request):
    """
    For example, the following code would send two different messages to two different sets of recipients; however, only one connection to the mail server would be opened.

    message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
    message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com'])
    send_mass_mail((message1, message2), fail_silently=False)
    The return value will be the number of successfully delivered messages.
    """
    if request.method == "POST":
        to_send = request.POST.getlist('patient')
    # this gets a list of patient IDs
    # TODO: get emails associated and send birthday email

    # datatuple is a tuple in which each element is in this format:
    # (subject, message, from_email, recipient_list)
    return HttpResponse(to_send)
    # send_mass_mail(datatuple, fail_silently=False)


def revoke(request):
    user = request.session.get("user", None)
    print user
    if user:
        api.revoke_token(user)
        # delete from db
        u = Doctor.objects.get(pk=user)
        u.delete()
        # remove from session
        del request.session["user"]

    return HttpResponse("token revoked")
