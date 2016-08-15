#### Handles API calls ###
import os, requests, datetime
from models import Doctor

def get_tokens(code, grant_type):
    """ Using auth code, get tokens for further needed API calls """
    # grant_types: 'authorization_code' or "refresh_token"
    payload = {
    'code': code,
    'grant_type': grant_type,
    'redirect_uri': 'http://127.0.0.1:8000/login',
    'client_id': os.environ["DRCHRONO_CLIENT_ID"],
    'client_secret': os.environ['DRCHRONO_CLIENT_SECRET'],
    }

    response = requests.post('https://drchrono.com/o/token/', data=payload)
    response.raise_for_status()
    return response.json()

def get_doctor(token):

    response = requests.get('https://drchrono.com/api/users/current', headers={
    'Authorization': 'Bearer %s' % token,
    })
    response.raise_for_status()
    data = response.json()

    # You can store this in your database along with the tokens
    username = data['username']

    return username

def get_patients(doctor):
    # doctor is an object
    # TODO: refresh token method.

    headers = {
    'Authorization': 'Bearer ' + doctor.access_token,
    }

    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next'] # A JSON null on the last page
    # print "patients", patients
    return patients

def revoke_token(user_id):
    token = Doctor.objects.get(pk=user_id).access_token
    payload = {
    'token': token,
    'client_id': os.environ["DRCHRONO_CLIENT_ID"],
    'client_secret': os.environ['DRCHRONO_CLIENT_SECRET'],
    }

    response = requests.post('https://drchrono.com/o/revoke_token/', data=payload)
