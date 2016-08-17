from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail



import api
import os, datetime, requests, json
from models import Doctor
from forms import RefillForm

# Create your views here.
def index(request):
    user = request.session.get("user", None)
    print user
    if user:
        return redirect("patients/")

    else:
        params = {"redirect": "http%3A//127.0.0.1%3A8000/medications/authorize",
                "client_id": os.environ["DRCHRONO_MEDS_CLIENT_ID"]}

        return render(request, "medications/index.html", params)


def authorize(request):
    """
    Handles authorizing application.  Stores drchrono API tokens in db
    """
    # redirect with the authorization codes from drchrono
    code = request.GET.get("code", "")

    # TODO: notify user that they need to authorize.
    if not code:
        return redirect("medications")

    # get doctor id
    doc_id = api.get_tokens(code)
    request.session['user'] = doc_id
    # redirect to patient listing page
    return redirect("patients/")


def patients(request):
    """
    View for patient list to access medications
    """
    doc = Doctor.objects.get(pk=request.session['user'])

    patients = api.get_patients(doc)

    return render(request, "medications/patients.html", {'patients': patients})

def patient_detail(request):
    """
    given a patient_id, returns medication information
    """
    patient_id = request.GET.get('patientId')
    # TODO: get patient medication information to list.
    # TODO: render refill option for each medication. maybe as modal?
    return HttpResponse("here's some details")
