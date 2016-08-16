from models import Doctor

def save_api_credentials(params):
    doc = Doctor(access_token = params['access_token'],
    refresh_token = params['refresh_token'],
    expiration = timezone.now() + datetime.timedelta(seconds=params['expires_in']))

    doc.save()
    
    return doc.id
