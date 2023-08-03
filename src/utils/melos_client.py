import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


class MockClient:

    def get_user_data(self, melos_id):
        return {
            'first_name': 'Firstname',
            'last_name': 'Lastname',
            'person_number': '199105050203',
        }

    def is_member(self, ssn):
        if ssn == '196001010101':
            return False
        else:
            return True

    def get_melos_id(self, ssn):
        return 100000


class ApiClient:

    def request_get(self, path, params=None):
        if params is not None:
            params['orgId'] = settings.MELOS_ORG_ID

        return requests.get(
            settings.MELOS_URL + "/" + path,
            auth=HTTPBasicAuth('admin', settings.MELOS_ADMIN),
            params=params,
        )

    def get_user_data(self, melos_id):
        r = self.request_get('user-by-id' + '/' + str(melos_id))
        if r.status_code == 200:
            response_json = r.json()

            # person_nr is None for exchange students with T-numbers.
            # This is becuase Melos stores their personnummer
            # in medlemsnr instead of person_number
            if response_json['Personnr'] is None:
                response_json['Personnr'] = response_json["Medlemsnr"]
            return {
                'first_name': response_json['Fornamn'],
                'last_name': response_json['Efternamn'],
                'person_number': response_json['Personnr']
            }

    def is_member(self, ssn):
        r = self.request_get('is-member/' + ssn)
        if r.status_code == 200:
            return r.json()['Member']
        else:
            return False

    def get_melos_id(self, ssn):
        parsed_ssn = ssn

        if (not isinstance(parsed_ssn, str)):
            parsed_ssn = ssn[0].strftime('%Y%m%d') + '-' + ssn[1]

        r = self.request_get('user' + '/' + parsed_ssn)

        if r.status_code == 200:
            return r.json()['Id']
        else:
            return False


class MelosClient:
    client = None

    @staticmethod
    def __setup():
        if MelosClient.client is None:
            if settings.IS_RUNNING_TEST:
                MelosClient.client = MockClient()
            else:
                MelosClient.client = ApiClient()

    @staticmethod
    def get_user_data(melos_id):
        MelosClient.__setup()
        return MelosClient.client.get_user_data(melos_id)

    @staticmethod
    def is_member(ssn):
        MelosClient.__setup()
        return MelosClient.client.is_member(ssn)

    @staticmethod
    def get_melos_id(ssn):
        MelosClient.__setup()
        return MelosClient.client.get_melos_id(ssn)
