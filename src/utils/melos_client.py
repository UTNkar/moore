import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


class MelosClient:

    @staticmethod
    def request_get(path, params=None):
        if params is not None:
            params['orgId'] = settings.MELOS_ORG_ID

        return requests.get(
                    settings.MELOS_URL + "/" + path,
                    auth=HTTPBasicAuth('admin', settings.MELOS_ADMIN),
                    params=params,
                )

    @staticmethod
    def get_user_data(melos_id):
        r = MelosClient.request_get('user' + '/' + str(melos_id))

        if r.status_code == 200:
            data = {}
            data['first_name'] = r.json()['Fornamn']
            data['last_name'] = r.json()['Efternamn']
            data['person_number'] = r.json()['Personnr']
            data['phone_number'] = r.json()['Tele2']
            data['email'] = r.json()['Epost']
            return data

    @staticmethod
    def is_member(ssn):
        r = MelosClient.request_get('user/validateMembership', {'ssn': ssn})
        return r.status_code == 204

    @staticmethod
    def get_melos_id(ssn):
        parsed_ssn = ssn

        if(not isinstance(parsed_ssn, str)):
            parsed_ssn = ssn[0].strftime('%Y%m%d') + '-' + ssn[1]

        r = MelosClient.request_get('user', {
            'ssn': parsed_ssn,
        })

        if r.status_code == 200:
            return r.json()['Id']
        else:
            return False
