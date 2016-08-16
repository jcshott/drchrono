from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail, send_mass_mail


import api, utils
import os, datetime, requests
from models import Doctor


def index(request):
    # show either the login/authorize app page or doc's page
    user = request.session.get("user", None)
    if user:
        return redirect("/patients")

    else:
        params = {"redirect": "http%3A//127.0.0.1%3A8000/bdayreminder/login",
                "client_id": os.environ["DRCHRONO_CLIENT_ID"]}

        return render(request, "bdayreminder/index.html", params)


def login(request):
    # redirect with the authorization codes from drchrono
    #TODO: error handling if not authorized

    code = request.GET.get("code", "")

    # get doctor object - either new or existing
    doc = utils.log_in_user(code)
    request.session['user'] = doc.id
    # redirect
    return redirect("bdayreminder/patients")

def patients(request):
    # get data for bday messages
    user_id = request.session['user']

    birthdays_today = utils.patients_with_bdays(user_id)
    # returns list of dicts {'name': name, 'dob': date_birth, 'email': email, 'cell': cell, 'home_phone': home_phone}
    # fake = api.get_patients(Doctor.objects.get(pk=user_id))
    text_patients = []
    email_patients = []
    call_patients = []
    contact_info_needed = []
    # print "birthdays_today", birthdays_today
    # if not birthdays_today:
    #     return render(request, "bdayreminder/patients.html", patients)

    for patient in birthdays_today:
        if patient['cell']:
            text_patients.append(patient)
        elif patient['email']:
            email_patients.append(patient)
        elif patient['home_phone']:
            call_patients.append(patient)
        else:
            contact_info_needed.append(patient)

    patients = {'patients': {"text": text_patients, "email": email_patients, "home_call": call_patients, "no_contact": contact_info_needed}}

    return render(request, "bdayreminder/patients.html", patients)

def send_messages(request):
    if request.method == "POST":
        # these are lists of strings ["email, fullname"]
        texts_to_send = request.POST.getlist("patient_text", [])
        emails_to_send = request.POST.getlist("patient_email", [])
        texts = []
        emails = []

        for item in texts_to_send:
            info = item.split(",")
            texts.append(info)

        for item in emails_to_send:
            info = item.split(",")
            emails.append(info)
        print "texts", texts
        print "emails", emails
    #### Here I'd use TWILIO to send text and send_mail() to send email ####
        messages_sent = {"messages_sent": {"texts": texts, "emails": emails}}
        # print messages_sent
        # return redirect('/success', messages_sent)
        return render(request, 'bdayreminder/success.html', messages_sent)


        # this is list of string tuples [(email, fullname)]
# def send_emails(request):
#     """
#     sends emails to selected patients
#     """
#     if request.method == "POST":
#         to_send_info = request.POST.getlist('emailsSend[]')
#         # this is list of string tuples [(email, fullname)]
#
#     messages_sent = []
#
#     for item in to_send_info:
#         item = str(item)
#
#         info = item.split(',')
#         name = info[1].strip(")").strip()
#         email = info[0].strip("(").strip()
#         messages_sent.append((name, email))
#
#     # print "emails that would be sent", messages_sent
#
#     sent_names = []
#     for item in messages_sent:
#         sent_names.append(item[0])
#
#     context = {"sent": sent_names}
#     request.session['emails'] = sent_names
#     return redirect('/success')
#
#     # return render(request, 'bdayreminder/success.html', context)
#
#
# def send_texts(request):
#     """ takes in list of cell numbers and sends "happy birthday" text.
#     not working right now, would likely use Twilio API for this
#     """
#     if request.method == "POST":
#         text_to_send_info = request.POST.getlist('textsSend[]')
#         print text_to_send_info
#
#     text_messages_sent = []
#
#     for item in text_to_send_info:
#         item = str(item)
#
#         info = item.split(',')
#         name = info[1].strip(")").strip()
#         cell = info[0].strip("(").strip()
#         print "name", name
#         print "cell", cell
#         text_messages_sent.append((name, cell))
#
#     # print "texts that would be sent", text_messages_sent
#     request.session['texts'] = text_messages_sent
#     return redirect('/success')

def success(request):
    # sent_names = texts + emails
    # context = {"sent": sent_names}
    # texts = request.session.get('texts', [])
    # emails = request.session.get('emails',[])

    return render(request, 'bdayreminder/success.html')


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
