from django.utils import timezone
import os, requests, datetime

from models import Doctor
from utils import save_api_credentials

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

    if data['error']:
        # handle user hitting cancel on authorization.
        pass

    else:
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

def api_request(type, url):
    pass
