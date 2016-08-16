from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail

import api
import os, datetime, requests
from models import Doctor

# Create your views here.
def index(request):
    user = request.session.get("user", None)
    if user:
        return redirect("/patients")

    else:
        params = {"redirect": "http%3A//127.0.0.1%3A8000/medications/authorize",
                "client_id": os.environ["DRCHRONO_MEDS_CLIENT_ID"]}

        return render(request, "medications/index.html", params)


def authorize(request):
    """
    Handles authorizing application.  Stores drchrono API tokens in db
    """
    # redirect with the authorization codes from drchrono
    #TODO: error handling if not authorized

    code = request.GET.get("code", "")

    # get doctor object - either new or existing
    doc_id = api.get_tokens(code)
    request.session['user'] = doc_id
    # redirect to patient listing page
    return redirect("medications/patients", doc_id)


def patients(request):
    """
    View for patient list to access medications
    """
    doc = Doctor.get(pk=request.session['user'])
    return HttpResponse("hello medications app")

def patient_detail(request, patient_id):
    return HttpResponse("here's some details")
