from django.utils import timezone

import datetime
import api

from models import Doctor

def log_in_user(code):
    tokens = api.get_tokens(code,'authorization_code')

    # this is a tuple (id, username) of logged_in_doc
    logged_in_doc_un = api.get_doctor(tokens['access_token'])

    # try finding doc already logged-in and update tokens with token refresh call.
    try:
        doc = Doctor.objects.get(username=logged_in_doc_un)
        doc.access_token = access_token = tokens['access_token']
        doc.refresh_token = tokens['refresh_token']
        doc.expiration = timezone.now() + datetime.timedelta(seconds=tokens['expires_in'])

    except Exception:
        # if new doc - save in DB
        doc = Doctor(username=logged_in_doc_un, access_token = tokens['access_token'],
        refresh_token = tokens['refresh_token'],
        expiration = timezone.now() + datetime.timedelta(seconds=tokens['expires_in']))

    doc.save()

    # return doc object
    return doc

def patients_with_bdays(doc_id):
    """ given doctor, return list of patient JSON objects for those who have bdays today"""
    patient_list = api.get_patients(Doctor.objects.get(pk=doc_id))

    output = []

    for p in patient_list:
        date_birth = p.get("date_of_birth", None)
        curr_day = datetime.date.today()
        if date_birth:
            date_lst = date_birth.split("-")
            month = int(date_lst[1])
            day = int(date_lst[2])
            # if month == curr_day.month and day == curr_day.day:
            # if month == curr_day.month:
            p_id = p['id']
            name = p['first_name'] + " " + p["last_name"]
            email = p['email']
            cell = p['cell_phone']
            home_phone = p['home_phone']
            output.append({'name': name, 'dob': date_birth, 'email': email, 'cell': cell, 'home_phone': home_phone, "patient_id": p_id})
    return output
