from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail



import api, utils
import os, datetime, requests, json
from models import Doctors, Patients, Medications
from forms import RefillForm

# Create your views here.
def index(request):
    user = request.session.get("user", None)
    print user
    if user:
        return redirect("patients/")

    else:
        params = {"redirect": "http%3A//127.0.0.1%3A8000/medications/authorize",
                "client_id": os.environ["DRCHRONO_MEDS_CLIENT_ID"],
                "scope": "user:read patients:read patients:write calendar:read calendar:write clinical:read clinical:write"}

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
    doc = utils.get_doctor(code)
    request.session['user'] = doc.doc_id
    # redirect to patient listing page
    return redirect("patients/")


def patients(request):
    """
    View for patient list to access medications
    """
    doc = Doctors.objects.get(doc_id=request.session.get("user"))

    patients = api.get_patients(doc)
    utils.check_new_patients(patients, doc)

    # patient meds is {"patient_id": {"id": patient_id, "name": patient_name, "curr_meds": [{"med_id": id_in_my_db, "med_name": name, "refills": number_refills_left}]}}
    patient_meds = utils.get_medications(patients, doc.access_token)

    return render(request, "medications/patients.html", {'patient_info': patient_meds})


def process_refill(request):

    med_id = int(request.POST.get('med_id'))
    medication_obj = Medications.objects.get(pk=med_id)
    medication_obj.number_refills = medication_obj.number_refills - 1
    medication_obj.save()

    return HttpResponse(medication_obj.number_refills)

def patient_detail(request):
    """
    given a patient_id, returns medication information
    """
    patient_id = request.GET.get('patientId')
    # TODO: get patient medication information to list.
    # TODO: render refill option for each medication. maybe as modal?
    return HttpResponse("here's some details")

def send_email(request):
    """
    handles sending email to patient notifiying need to make appt for meds
    """
    pass
