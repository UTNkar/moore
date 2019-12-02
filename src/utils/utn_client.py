
import requests
from requests.auth import HTTPDigestAuth
from django.conf import settings


class UTNClient:

    @staticmethod
    def registration_status(ssn):
        r = requests.get(
            'https://register.utn.se/api.php',
            auth=HTTPDigestAuth(settings.MEMBERSHIP_API_USER,
                                settings.MEMBERSHIP_API_PASSWORD),
            params={
                'action': 'check',
                'person_number': ssn
            },
        )

        try:
            return r.json().get('status')
        except requests.exceptions.ConnectionError:
            return 'unknown'
