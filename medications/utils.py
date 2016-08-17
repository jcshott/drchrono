
from models import Doctors, Patients, Medications

import api

def get_doctor(tokens):
    """
    input - auth code.
    Checks if doctor is in our db. if not, adds to db
    Return - doctor object from db
    """
    # check if we know this doctor
    #TODO: this would be better to store a cookie or something w/username when first authorize so don't need to use API call each time.

    current_doc_info = api.get_doctor_info(tokens['access_token'])
    # try finding doc already logged-in and update tokens with token refresh call.
    try:
        doc = Doctors.objects.get(doc_id=current_doc_info['id'])
        # TODO: REFRESH token if needed
        # doc.access_token = access_token = tokens['access_token']
        # doc.refresh_token = tokens['refresh_token']
        # doc.expiration = timezone.now() + datetime.timedelta(seconds=tokens['expires_in'])

    except Exception:
        # if new doc - save in DB
        doc = Doctors(doc_id=current_doc_info['id'],
        username=current_doc_info['username'],
        access_token = tokens['access_token'],
        refresh_token = tokens['refresh_token'],
        expiration = tokens['expires_timestamp'])

        doc.save()

    # return doc object
    return doc

def check_new_patients(patient_list, doc):
    """
    Input: current patient list when doc comes to site

    Checks if any new patients to add to our db.
    If so, grabs their medication information and adds to db.

    output: None
    """
    for patient in patient_list:
        try:
            Patients.objects.get(patient_id=patient['id'])
        except Exception as e:
            new_patient = Patients(patient_id=patient['id'], first_name=patient['first_name'], last_name=patient['last_name'], primary_doc=doc, cell_phone=patient['cell_phone'],email=patient['email'])

            new_patient.save()

def get_medications(patient_list, access_token):
    """
    Input: list of patient objects
    Output: dict of patient_id: name, list of dicts of med info.

    ex. {"123": "name": Joe Schmoe, "curr_meds": [{med_name: humira, refills: 3}, {med_name: oxycodone, refills: 0}]}
    """
    patient_med_info =[]
    # API request for medications for each patient. Ideally this would be done in background when doc authorizes app so that you can spread out the API requests.

    for patient in patient_list:
        p_id = patient['id']
        patient_obj = Patients.objects.get(patient_id=p_id)
        p_first_name = patient['first_name']
        p_last_name = patient['last_name']
        current_meds = api.api_get_medications(p_id, access_token)
        med_temp = []
        for med in current_meds:
            if med.get("status", "ok") != "inactive":
                try:
                    # get the listing in our db first, if present as it will have up to date refills
                    try_med_obj = Medications.objects.filter(patient_id=patient_obj, name=med['name'])
                    med_obj = try_med_obj[0]
                except Exception as e:

                        # add new medication to db.
                        number_refills = med.get("number_refills", 0)
                        if number_refills == None:
                            number_refills = 0

                        med_obj = Medications(name=med['name'],
                        patient_id=patient_obj, number_refills=number_refills)
                        med_obj.save()

                med_name = med_obj.name
                refills = med_obj.number_refills
                med_temp.append({"med_id": med_obj.id, "med_name": med_name, "refills": refills})

        # build patient entry in full med_info
        patient_med_info.append({"id": p_id, "name": p_first_name + " " + p_last_name, "current_meds": med_temp})

    return patient_med_info
