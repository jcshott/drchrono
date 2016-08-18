from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages

from django.contrib.sessions.models import Session


import api, utils
import os, datetime, requests, json
from models import Doctors, Patients, Medications
from forms import RenewalForm

# Create your views here.
def index(request):

    user = request.session.get("user", None)

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

    if not code:
        messages.error(request, 'Please Authorize this Application with drchrono.')

        params = {"redirect": "http%3A//127.0.0.1%3A8000/medications/authorize",
                "client_id": os.environ["DRCHRONO_MEDS_CLIENT_ID"],
                "scope": "user:read patients:read patients:write calendar:read calendar:write clinical:read clinical:write"}

        return render(request, "medications/index.html", params)

    tokens = api.get_tokens(code)
    # get doctor id
    doc = utils.get_doctor(tokens)
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
    print request.POST
    med_id = int(request.POST.getlist('med_id')[0])
    medication_obj = Medications.objects.get(pk=med_id)
    medication_obj.update_refill_amt(-1)
    # medication_obj.save()

    return HttpResponse(medication_obj.number_refills)

def process_renewal(request):
    if request.method == "POST":
        # returns a list of the selected action.
        selection = request.POST.getlist('action')[0]
        # print request.POST
        #utils.send_appt_email()
        med_id = request.POST.get('med_id')
        if selection == "approve":
            # process autorenewal
            renew_amt = request.POST.getlist('renew_amt')[0]
            # # update db to reflect renewal
            medication_obj = Medications.objects.get(pk=med_id)
            medication_obj.update_refill_amt(int(renew_amt))
            # medication_obj.save()
        else:
            utils.send_appt_email()
        return HttpResponse("thanks")
    else:
        med_id = int(request.GET.get('med_id'))
        form = RenewalForm()
        form.fields['med_id'].initial = med_id
        return render(request, 'medications/renewal.html', {'form': form})


def make_appointment(request):

    return HttpResponse("here you'd be able to make an appointment")

def test_api(request):
    doc = Doctors.objects.get(doc_id=request.session.get("user"))
    api.api_test(doc.access_token)
