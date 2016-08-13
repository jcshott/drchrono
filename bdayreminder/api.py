#### Handles API calls ###
import os, requests, datetime
from models import Doctor

def get_tokens(code):
    """ Using auth code, get tokens for further needed API calls """

    payload = {
    'code': code,
    'grant_type': 'authorization_code',
    'redirect_uri': 'http://127.0.0.1:8000/api_auth',
    'client_id': os.environ["DRCHRONO_CLIENT_ID"],
    'client_secret': os.environ['DRCHRONO_CLIENT_SECRET'],
    }

    response = requests.post('https://drchrono.com/o/token/', data=payload)
    response.raise_for_status()
    return response.json()

def get_patients(doctor):
    # doctor is an object
    headers = {
    'Authorization': 'Bearer ' + doctor.access_token,
    }
    # headers = {
    # 'Authorization': 'Bearer KMPZ7KxtlUxlM102HXP7kZi94OXlMm',
    # }

    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next'] # A JSON null on the last page

    return patients

def revoke_token(user_id):
    token = Doctor.objects.get(pk=user_id).access_token
    payload = {
    'token': token,
    'client_id': os.environ["DRCHRONO_CLIENT_ID"],
    'client_secret': os.environ['DRCHRONO_CLIENT_SECRET'],
    }

    response = requests.post('https://drchrono.com/o/revoke_token/', data=payload)
