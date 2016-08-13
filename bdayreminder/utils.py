import datetime
import api

from models import Doctor

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
            if month == curr_day.month:
                output.append(p)
    return output
