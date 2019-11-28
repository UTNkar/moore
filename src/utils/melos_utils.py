import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def melos_request_get(path, params):
    if params is not None:
        params['orgId'] = settings.MELOS_ORG_ID

    return requests.get(
                settings.MELOS_URL + "/" + path,
                auth=HTTPBasicAuth('admin', settings.MELOS_ADMIN),
                params=params,
            )

def melos_user_data(melos_id):
    r = melos_request_get('user' + '/' + str(melos_id))
    
    if r.status_code == 200:
        data = {}
        data['first_name'] = r.json()['Fornamn']
        data['last_name'] = r.json()['Efternamn']
        data['person_number'] = r.json()['Personnr']
        data['phone_number'] = r.json()['Tele2']
        data['email'] = r.json()['Epost']
        return data


def melos_is_member(ssn):
    r = melos_request_get('user/validateMembership', { 'ssn': ssn })
    return r.status_code == 204

def find_melos_id(ssn):
    parsed_ssn = ssn

    if(not isinstance(parsed_ssn, str)):
        parsed_ssn = ssn[0].strftime('%Y%m%d') + '-' + ssn[1]

    r = melos_request_get('user', {
        'ssn': parsed_ssn,
    })

    if r.status_code == 200:
        return r.json()['Id']
    else:
        return False