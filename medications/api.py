from django.utils import timezone
import os, requests, datetime

from models import Doctor
import utils

def get_tokens(code):
    """
    OAuth Req. for tokens
    """
    payload = {
    'code': code,
    'grant_type': 'authorization_code',
    'redirect_uri': 'http://127.0.0.1:8000/medications/authorize',
    'client_id': os.environ['DRCHRONO_MEDS_CLIENT_ID'],
    'client_secret': os.environ['DRCHRONO_MEDS_CLIENT_SECRET'],
    }

    response = requests.post('https://drchrono.com/o/token/', data=payload)
    response.raise_for_status()
    data = response.json()

    # Save info for user
    user_token_info = {'access_token': data['access_token'],
    'refresh_token': data['refresh_token'],
    'expires_timestamp': timezone.now() + datetime.timedelta(seconds=data['expires_in'])
    }
    doc_id = utils.save_api_credentials(user_token_info)
    return doc_id


def refresh_token(user):
    """
    Refresh API tokens
    """
    # TODO: refresh token get.
    refresh_token = user.get_refresh()
    params = {
    'refresh_token': refresh_token,
    'grant_type': 'refresh_token',
    'client_id': os.enviorn['DRCHRONO_MEDS_CLIENT_ID'],
    'client_secret': os.environ['DRCHRONO_MEDS_CLIENT_SECRET'],
    }

    response = requests.post('https://drchrono.com/o/token/', data=params)
    response.raise_for_status()
    data = response.json()

    # TODO: UPDATE these in your database associated with the user
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])

def get_patients(doc):
    """
    general drchrono API request function

    """

    access_token = doc.access_token
    headers = { 'Authorization': "Bearer " + access_token,}

    patients = []
    patients_url = 'https://drchrono.com/api/patients_summary'
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next'] # A JSON null on the last page
    return patients
