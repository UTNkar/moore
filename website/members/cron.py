import kronos
import requests
from django.conf import settings
from requests.auth import HTTPDigestAuth

from members.models import Member


@kronos.register('0 3 * * 1')  # At 03:00 on Monday.
def update_membership_status():
    r = requests.get(
        'https://register.utn.se/api.php',
        auth=HTTPDigestAuth(settings.MEMBERSHIP_API_USER,
                            settings.MEMBERSHIP_API_PASSWORD),
        params={
            'action': 'list',
        },
    )
    try:
        data = r.json()
    except ValueError:
        return

    for member in Member.objects.all():
        if member.person_number().replace('-', '') in data:
            member.update_status(data='member')
        else:
            member.update_status(data='nonmember')
        Member.objects.filter(pk=member.pk).update(
            status=member.status, status_changed=member.status_changed
        )
