
from models import Doctor


def save_api_credentials(params):
    doc = Doctor(access_token = params['access_token'],
    refresh_token = params['refresh_token'],
    expiration = params['expires_timestamp'])

    doc.save()

    return doc.id
